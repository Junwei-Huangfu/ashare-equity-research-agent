"""Skill 6b: Reviewer + reviser agents — the multi-agent quality loop.

    writer (flash, thinking off)  ->  draft
    evaluator (Python rules)      ->  untraceable numbers, invalid citations ...
    reviewer (v4-pro, thinking ON)->  issue list: contradictions, selective use of evidence,
                                      wrong comparisons, ambiguous wording, numbers the model computed
    reviser  (flash, thinking off)->  final report, fixing the issues one by one
    evaluator + reviewer again    ->  measure what is left  (--verify)

Why two different models: the writer only re-organises facts Python already computed, so a fast model
without thinking is enough. Reviewing means cross-checking the whole text against the data, which needs
real reasoning, so the reviewer is the stronger model with thinking switched on.

Input : reports/{code}_draft.md, reports/{code}_facts.json, reports/{code}_eval_{code}_draft.json
Output: reports/{code}_review.json          reviewer's issue list (+ its reasoning in _review_thinking.md)
        reports/{code}_final.md             revised report
        reports/{code}_review_final.json    (--verify) reviewer's issue list on the final report

Usage (run from the project root):
    python skills/evaluation/evaluate.py                 # 1. rule-based check of the draft
    python skills/report_writer/review.py                # 2. review + revise -> final.md
    python skills/evaluation/evaluate.py reports/sz000538_final.md
    python skills/report_writer/review.py --verify       # 3. review the final report again (count what is left)
"""
import json
import os
import re
import sys
import time
import tomllib
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS = PROJECT_ROOT / "reports"
CONFIG = PROJECT_ROOT / "config" / "report.toml"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "report_writer"))
from writer import SYSTEM_PROMPT as WRITER_RULES, TARGET  # noqa: E402

REVIEW_PROMPT = """你是卖方研究所的资深审稿人（质量控制），负责审阅AI生成的公司深度报告初稿。
你会收到：①事实数据包（唯一可信的数据来源，含年报证据）②自动评测结果 ③报告初稿。
请逐段通读初稿，对照事实数据包，找出以下问题：
A. 数字问题：数字与数据包不一致，或数据包中不存在（模型自行计算的差值、比例也算）。
B. 前后矛盾：同一事实在不同段落说法不一致；标题、投资要点与正文结论不一致。
C. 选择性引用 / 口径误用：只挑对结论有利的证据；忽略数据包中已说明的口径差异；把母公司或特定口径的数字当成整体结论。
D. 比较结论错误：排名、高低、同业比较与"同业排名""本公司与同业中位数比较"不一致。
E. 表述歧义或不专业：容易被误解的说法（如把WACC区间上沿和价值区间上沿混淆）。
F. 违反写作规则：评级或区间被修改；年报证据已回答却仍标"待年报验证"；年报证据不足却当作事实陈述。
要求：只报告真实存在的问题，不要为了凑数报告；每个问题必须引用初稿原文（quote，不超过40字）并说明数据包中的依据。
severity：高=会误导投资判断；中=影响专业性或一致性；低=措辞小问题。
只输出 JSON：
{"overall": "一句话总体评价",
 "issues": [{"id": 1, "severity": "高", "type": "C", "location": "章节", "quote": "原文", "problem": "问题", "evidence": "数据包依据", "fix": "修改建议"}]}"""

REVISE_PROMPT = WRITER_RULES + """

你现在的任务是【修订】：根据审稿意见修改报告初稿。
1. 逐条处理审稿意见中的每个问题；没有被指出问题的段落保持原样，不要重写全文风格。
2. 修订时同样只能使用事实数据包中的数字，不得引入新数字。
3. 输出修订后的完整报告（Markdown），不要输出修订说明。"""


def client_and_cfg():
    from openai import OpenAI
    load_dotenv(PROJECT_ROOT / ".env")
    client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
    return client, tomllib.load(open(CONFIG, "rb"))


def parse_json(text: str) -> dict:
    """The reviewer may wrap JSON in prose or ```json fences: take the outermost {...}."""
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else {"overall": "unparsable", "issues": []}
    except json.JSONDecodeError:
        return {"overall": "unparsable", "issues": [], "raw": text}


def review(client, cfg: dict, report_path: Path, eval_path: Path) -> tuple[dict, str, dict]:
    facts = (REPORTS / f"{TARGET}_facts.json").read_text(encoding="utf-8")
    ev = eval_path.read_text(encoding="utf-8") if eval_path.exists() else "{}"
    user = (f"【事实数据包】\n```json\n{facts}\n```\n\n【自动评测结果】\n```json\n{ev}\n```\n\n"
            f"【报告初稿】\n{report_path.read_text(encoding='utf-8')}")
    r = cfg["review"]
    t0 = time.time()
    resp = client.chat.completions.create(
        model=r["model"], max_tokens=r["max_tokens"],
        messages=[{"role": "system", "content": REVIEW_PROMPT}, {"role": "user", "content": user}],
        extra_body={"thinking": {"type": r["thinking"]}},
    )
    msg = resp.choices[0].message
    usage = {"model": r["model"], "seconds": round(time.time() - t0, 1),
             "prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens,
             "finish_reason": getattr(resp.choices[0], "finish_reason", None)}
    return parse_json(msg.content), getattr(msg, "reasoning_content", None) or "", usage


def revise(client, cfg: dict, draft: str, issues: dict) -> tuple[str, dict]:
    facts = (REPORTS / f"{TARGET}_facts.json").read_text(encoding="utf-8")
    user = (f"【审稿意见】\n```json\n{json.dumps(issues, ensure_ascii=False, indent=1)}\n```\n\n"
            f"【报告初稿】\n{draft}\n\n【事实数据包】\n```json\n{facts}\n```")
    r = cfg["revise"]
    t0 = time.time()
    resp = client.chat.completions.create(
        model=r["model"], temperature=r["temperature"], max_tokens=r["max_tokens"],
        messages=[{"role": "system", "content": REVISE_PROMPT}, {"role": "user", "content": user}],
        extra_body={"thinking": {"type": r["thinking"]}},
    )
    text = resp.choices[0].message.content or ""
    if not text.strip():
        raise RuntimeError("Reviser returned an empty report.")
    return text, {"model": r["model"], "seconds": round(time.time() - t0, 1),
                  "prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens,
                  "finish_reason": getattr(resp.choices[0], "finish_reason", None)}


def show_issues(result: dict) -> None:
    issues = result.get("issues", [])
    by_sev = {s: sum(i.get("severity") == s for i in issues) for s in ["高", "中", "低"]}
    print(f"  Overall: {result.get('overall')}")
    print(f"  Issues: {len(issues)}  (高 {by_sev['高']} / 中 {by_sev['中']} / 低 {by_sev['低']})")
    for i in issues:
        print(f"   [{i.get('severity')}][{i.get('type')}] {i.get('location')}: 「{i.get('quote')}」")
        print(f"        problem: {i.get('problem')}")
        print(f"        fix    : {i.get('fix')}")


if __name__ == "__main__":
    client, cfg = client_and_cfg()
    verify = "--verify" in sys.argv
    name = "final" if verify else "draft"
    report_path = REPORTS / f"{TARGET}_{name}.md"
    eval_path = REPORTS / f"{TARGET}_eval_{TARGET}_{name}.json"
    out_name = "review_final" if verify else "review"

    print(f"Reviewing {report_path.name} with {cfg['review']['model']} (thinking {cfg['review']['thinking']}) "
          f"... this can take a few minutes")
    result, thinking, usage = review(client, cfg, report_path, eval_path)
    result["usage"] = usage
    (REPORTS / f"{TARGET}_{out_name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if thinking:
        (REPORTS / f"{TARGET}_{out_name}_thinking.md").write_text(thinking, encoding="utf-8")
    print(f"Done in {usage['seconds']}s  tokens in/out: {usage['prompt_tokens']:,} / {usage['completion_tokens']:,}")
    show_issues(result)
    print(f"Saved -> reports/{TARGET}_{out_name}.json")

    if verify or not result.get("issues"):
        sys.exit(0)

    print(f"\nRevising with {cfg['revise']['model']} ...")
    final, rusage = revise(client, cfg, report_path.read_text(encoding="utf-8"), result)
    (REPORTS / f"{TARGET}_final.md").write_text(final, encoding="utf-8")
    (REPORTS / f"{TARGET}_final_usage.json").write_text(json.dumps(rusage, indent=2), encoding="utf-8")
    print(f"Done in {rusage['seconds']}s  tokens in/out: {rusage['prompt_tokens']:,} / {rusage['completion_tokens']:,}")
    print(f"Saved -> reports/{TARGET}_final.md")
    print("Next: python skills/evaluation/evaluate.py reports/" + f"{TARGET}_final.md")