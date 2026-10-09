"""Skill 5c: Annual-report RAG — answer research questions from the annual reports, with page citations.

For every question in config/rag_questions.toml:
  1. Retrieve: run several search queries (multi-query), merge the hits, down-weight accounting-policy
     boilerplate, keep the best chunk per page, take the top N as evidence.
  2. Answer : the LLM may ONLY use the evidence and must cite (year, page) for every claim;
              if the evidence is not enough it must say so (sufficient = false).
  3. Check  : every citation must point to a page that was actually given as evidence,
              otherwise it is flagged as an invalid (hallucinated) citation.

Output: reports/{code}_annual_report_qa.json   (answers + citations + evidence, read by the report writer)
        reports/{code}_annual_report_qa.md     (human-readable)

Usage (run from the project root):
    python skills/annual_report_rag/qa.py --dry-run    # retrieval only: shows the evidence pages, no API cost
    python skills/annual_report_rag/qa.py              # retrieval + LLM answers
"""
import json
import os
import sys
import time
import tomllib
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG = PROJECT_ROOT / "config" / "rag_questions.toml"
REPORTS = PROJECT_ROOT / "reports"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "annual_report_rag"))
from index import TARGET, Index, load_chunks, load_tokens  # noqa: E402

SYSTEM_PROMPT = """你是严谨的卖方研究员助理，任务是根据上市公司年报原文片段回答问题。
规则：
1. 只能使用提供的【证据】片段，不得使用你自己的知识，不得编造任何数字或事实。
2. 每个关键事实后用括号注明出处，格式：（2025年报第198页）。只能引用提供的证据中出现过的年份和页码。
3. 数字必须与原文一致；可以把"元"换算为"亿元"，但需保留两位小数。
4. 如果证据不足以回答问题的某部分，明确写出"年报片段未提供XX信息"，并把 sufficient 设为 false。
5. 回答用中文，150-300字，先给结论再给依据。
只输出 JSON：{"answer": "...", "citations": [{"year": 2025, "page": 198}], "sufficient": true}"""


def retrieve(index: Index, q: dict, cfg: dict) -> list[dict]:
    r = cfg["retrieval"]
    best = {}
    for query in q["queries"]:
        for h in index.search(query, q["years"], k=r["k_per_query"]):
            score = h["score"] * (r["policy_penalty"] if ("会计政策" in h["text"] or "会计估计" in h["text"]) else 1)
            if h["id"] not in best or score > best[h["id"]]["score"]:
                best[h["id"]] = {**h, "score": round(score, 2), "query": query}
    per_page = {}                                    # overlapping chunks of one page -> keep the best one
    for h in sorted(best.values(), key=lambda x: x["score"], reverse=True):
        per_page.setdefault((h["year"], h["page"]), h)
    return list(per_page.values())[: r["max_evidence"]]


def build_user_prompt(q: dict, evidence: list[dict]) -> str:
    blocks = [f"[E{i + 1}] {e['year']}年报 第{e['page']}页（{e['section']}）\n{e['text']}" for i, e in enumerate(evidence)]
    return f"【问题】{q['question']}\n\n【证据】\n" + "\n\n".join(blocks)


def ask(client, model: str, q: dict, evidence: list[dict], cfg: dict) -> dict:
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": build_user_prompt(q, evidence)}],
        temperature=cfg["llm"]["temperature"], max_tokens=cfg["llm"]["max_tokens"],
        response_format={"type": "json_object"},
        extra_body={"thinking": {"type": cfg["llm"]["thinking"]}},
    )
    try:
        out = json.loads(resp.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        out = {"answer": resp.choices[0].message.content or "", "citations": [], "sufficient": False}
    given = {(e["year"], e["page"]) for e in evidence}
    cites = [(int(c.get("year", 0)), int(c.get("page", 0))) for c in out.get("citations", []) if isinstance(c, dict)]
    out["valid_citations"] = [f"{y}年报第{p}页" for y, p in cites if (y, p) in given]
    out["invalid_citations"] = [f"{y}年报第{p}页" for y, p in cites if (y, p) not in given]
    out["seconds"] = round(time.time() - t0, 1)
    out["tokens"] = {"in": resp.usage.prompt_tokens, "out": resp.usage.completion_tokens}
    return out


def to_markdown(results: list[dict]) -> str:
    md = [f"# 年报问答（RAG）：{TARGET}\n", "每个回答只基于检索到的年报原文片段，括号内为出处。\n"]
    for r in results:
        md.append(f"## {r['question']}\n")
        a = r.get("llm")
        if a:
            flag = "" if a.get("sufficient") else "（证据不足，部分信息年报片段未覆盖）"
            md.append(f"{a['answer']}{flag}\n")
            md.append(f"- 有效引用：{', '.join(a['valid_citations']) or '无'}")
            if a["invalid_citations"]:
                md.append(f"- ⚠ 无效引用（不在证据中）：{', '.join(a['invalid_citations'])}")
        md.append("- 检索到的证据页：" + "；".join(f"{e['year']}年报第{e['page']}页" for e in r["evidence"]) + "\n")
    return "\n".join(md)


if __name__ == "__main__":
    load_dotenv(PROJECT_ROOT / ".env")
    cfg = tomllib.load(open(CONFIG, "rb"))
    dry = "--dry-run" in sys.argv

    chunks = load_chunks(TARGET)
    index = Index(chunks, load_tokens(chunks))
    client = model = None
    if not dry:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
        model = os.environ["LLM_MODEL"]

    results = []
    for q in cfg["question"]:
        evidence = retrieve(index, q, cfg)
        print(f"\n[{q['id']}] {q['question']}")
        for e in evidence:
            print(f"   {e['year']}年报 第{e['page']:>3}页  score {e['score']:>6}  {e['text'][:60]}")
        item = {"id": q["id"], "question": q["question"], "years": q["years"],
                "evidence": [{k: e[k] for k in ("id", "year", "page", "section", "score", "query", "text")}
                             for e in evidence]}
        if not dry:
            item["llm"] = ask(client, model, q, evidence, cfg)
            a = item["llm"]
            print(f"   -> answered in {a['seconds']}s, sufficient={a.get('sufficient')}, "
                  f"valid citations {len(a['valid_citations'])}, invalid {len(a['invalid_citations'])}")
        results.append(item)

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"{TARGET}_annual_report_qa.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS / f"{TARGET}_annual_report_qa.md").write_text(to_markdown(results), encoding="utf-8")
    print(f"\nSaved -> reports/{TARGET}_annual_report_qa.json, reports/{TARGET}_annual_report_qa.md"
          + ("   (dry run: evidence only, no answers)" if dry else ""))