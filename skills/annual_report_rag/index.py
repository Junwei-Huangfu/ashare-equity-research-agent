"""Skill 5b: Annual-report RAG — split the annual reports into page-tagged chunks and search them with BM25.

Why BM25 (keyword search) and not vector search:
  DeepSeek's official API offers chat models only, no embedding model. BM25 needs no extra API,
  is free and works well on annual reports, whose terms are very standardised (销售费用, 长期股权投资 ...).
  search() is the only retrieval function, so it can later be swapped for vector search.

Steps:
  1. Read every page of data/raw/annual_reports/{code}_{year}.pdf with PyMuPDF.
  2. Clean: drop the repeated page header ("...年年度报告全文") and the page-number line; join broken lines.
  3. Chunk each page into ~400-character pieces with 100 characters of overlap (sentences cut at a
     chunk border still appear whole in the neighbouring chunk). Every chunk keeps year + page + section.
  4. Tokenise Chinese with jieba search mode (plus a small finance dictionary) and rank chunks with BM25.

Output: data/processed/rag/chunks.jsonl + tokens.json   (git-ignored, rebuilt from the PDFs)

Usage (run from the project root):
    python skills/annual_report_rag/index.py                          # build the index + demo search
    python skills/annual_report_rag/index.py "销售费用 增加 原因" 2025   # search your own query (year optional)
    python skills/annual_report_rag/index.py --rebuild                # re-read the PDFs
"""
import json
import logging
import re
import sys
from pathlib import Path

import jieba
import pymupdf
from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = PROJECT_ROOT / "data" / "raw" / "annual_reports"
RAG_DIR = PROJECT_ROOT / "data" / "processed" / "rag"
CHUNKS = RAG_DIR / "chunks.jsonl"
TOKENS = RAG_DIR / "tokens.json"      # cache: jieba tokenisation of every chunk (slow to recompute)

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]
CHUNK_SIZE = 400
OVERLAP = 100
MIN_PAGE_CHARS = 50

jieba.setLogLevel(logging.WARNING)
# Finance terms that jieba would otherwise cut into pieces
for w in ["销售费用", "管理费用", "研发费用", "财务费用", "营业收入", "营业成本", "毛利率", "净利润",
          "归属于上市公司股东的净利润", "经营活动产生的现金流量净额", "长期股权投资", "交易性金融资产",
          "应收账款", "应收票据", "存货", "合同负债", "权益法", "公允价值变动", "投资收益", "非经常性损益",
          "医药商业", "医药工业", "工业销售", "商业销售", "健康品", "中药资源", "三七", "牙膏",
          "上海医药", "云南白药", "集采", "医保", "国家保密配方", "品牌推广", "市场推广费", "广告宣传费"]:
    jieba.add_word(w)

STOP = set("的 了 和 与 及 或 等 为 在 对 以 是 由 其 中 上 下 年 月 日 本 该 公司 报告 报告期 期内 情况 主要 相关".split())
SECTION_RE = re.compile(r"^第[一二三四五六七八九十]+节\s*\S+")


# ---------------------------------------------------------------- 1-3. PDF -> chunks
def clean_page(text: str) -> tuple[str, list[str]]:
    """Remove header/page-number lines, join broken lines. Returns (clean text, section headings found)."""
    lines, headings = [], []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or "年度报告全文" in s or re.fullmatch(r"\d{1,3}", s):
            continue
        if SECTION_RE.match(s) and "...." not in s:
            headings.append(SECTION_RE.match(s).group(0))
        lines.append(s)
    return "".join(lines), headings          # Chinese text: lines are simply concatenated


def chunk_text(text: str) -> list[str]:
    if len(text) <= CHUNK_SIZE:
        return [text]
    step = CHUNK_SIZE - OVERLAP
    return [text[i:i + CHUNK_SIZE] for i in range(0, max(len(text) - OVERLAP, 1), step)]


def build_chunks(code: str) -> list[dict]:
    chunks = []
    for pdf in sorted(PDF_DIR.glob(f"{code}_*.pdf")):
        year = int(pdf.stem.split("_")[-1])
        section = "未识别章节"
        doc = pymupdf.open(pdf)
        for i, page in enumerate(doc):
            text, headings = clean_page(page.get_text())
            if len(headings) == 1:            # a page with many headings is the table of contents
                section = headings[0]
            if len(text) < MIN_PAGE_CHARS:
                continue
            for j, piece in enumerate(chunk_text(text)):
                chunks.append({"id": f"{year}-p{i + 1}-{j}", "year": year, "page": i + 1,
                               "section": section, "text": piece})
        doc.close()
        print(f"  {pdf.name}: {sum(c['year'] == year for c in chunks)} chunks")
    return chunks


def load_chunks(code: str, rebuild: bool = False) -> list[dict]:
    if CHUNKS.exists() and not rebuild:
        return [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").splitlines()]
    RAG_DIR.mkdir(parents=True, exist_ok=True)
    print("Building chunks from PDFs ...")
    chunks = build_chunks(code)
    CHUNKS.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in chunks), encoding="utf-8")
    print(f"Saved {len(chunks)} chunks -> {CHUNKS.relative_to(PROJECT_ROOT)}")
    return chunks


# ---------------------------------------------------------------- 4. BM25 search
def tokenize(text: str) -> list[str]:
    """jieba SEARCH mode: long words are also split into their parts, e.g. 上海医药 -> 上海 / 医药 / 上海医药.
    Used for both chunks and queries, so "上海医药" still matches a page that says "上海医药集团".
    """
    return [t for t in jieba.lcut_for_search(text)
            if len(t.strip()) > 1 and t not in STOP and not re.fullmatch(r"\W+", t)]


def load_tokens(chunks: list[dict], rebuild: bool = False) -> list[list[str]]:
    if TOKENS.exists() and not rebuild:
        tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
        if len(tokens) == len(chunks):
            return tokens
    print("Tokenising chunks with jieba (first run only, may take a minute) ...")
    tokens = [tokenize(c["text"]) for c in chunks]
    TOKENS.write_text(json.dumps(tokens, ensure_ascii=False), encoding="utf-8")
    return tokens


class Index:
    """BM25 over all chunks. search() can filter by fiscal year."""

    def __init__(self, chunks: list[dict], tokens: list[list[str]]):
        self.chunks = chunks
        self.bm25 = BM25Okapi(tokens)

    def search(self, query: str, years: list[int] | None = None, k: int = 5) -> list[dict]:
        scores = self.bm25.get_scores(tokenize(query))
        ranked = sorted(range(len(self.chunks)), key=lambda i: scores[i], reverse=True)
        hits = []
        for i in ranked:
            c = self.chunks[i]
            if years and c["year"] not in years:
                continue
            if scores[i] <= 0:
                break
            hits.append({**c, "score": round(float(scores[i]), 2)})
            if len(hits) == k:
                break
        return hits


def show(hits: list[dict], width: int = 160) -> None:
    for h in hits:
        print(f"  [{h['year']}年报 第{h['page']}页 | {h['section']} | score {h['score']}]")
        print(f"    {h['text'][:width]}...")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--rebuild"]
    rebuild = "--rebuild" in sys.argv
    chunks = load_chunks(TARGET, rebuild)
    print(f"Indexing {len(chunks)} chunks with BM25 ...")
    index = Index(chunks, load_tokens(chunks, rebuild))

    if args:   # ad-hoc query: index.py "query words" [year]
        query = args[0]
        years = [int(a) for a in args[1:]] or None
        print(f"\nQuery: {query}   years: {years or 'all'}")
        show(index.search(query, years))
    else:      # demo queries
        for q, yrs in [("销售费用 增加 原因 广告 推广", [2025]),
                       ("长期股权投资 上海医药 权益法", [2022]),
                       ("应收账款 增加 原因", [2021, 2022])]:
            print(f"\nQuery: {q}   years: {yrs}")
            show(index.search(q, yrs, k=3))