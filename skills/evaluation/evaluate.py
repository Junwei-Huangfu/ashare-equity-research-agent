"""Skill 7: Evaluation — rule-based quality checks on a generated report (no LLM, no cost, fully reproducible).

Checks
  1. Number traceability : every number in the report must appear in the facts pack
                           (which also contains the annual-report RAG answers). Untraceable numbers are
                           either computed by the model (forbidden) or hallucinated.
  2. Page citations      : every "20XX年报第N页" must be a page that passed the RAG citation check.
  3. Rating & range      : the rating and fair-value range in the report must equal the rule-based ones.
  4. Structure           : all seven required sections are present.
  5. Open items          : how many "待年报验证" remain (information still unverified).

Lessons from project 1 built in: section numbers ("5.1") and list numbers are not data;
years, dates, ranks ("第2/5") and page references are handled separately, not as data.

Input : a report .md, reports/{code}_facts.json, reports/{code}_annual_report_qa.json
Output: reports/{code}_eval_{report name}.json

Usage (run from the project root):
    python skills/evaluation/evaluate.py                                   # evaluates reports/{code}_draft.md
    python skills/evaluation/evaluate.py reports/sz000538_draft_v1.md reports/sz000538_draft_v3.md   # compare
"""
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS = PROJECT_ROOT / "reports"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]
REQUIRED_SECTIONS = ["一、", "二、", "三、", "四、", "五、", "六、", "七、"]
RATINGS = ["买入", "增持", "中性", "减持", "卖出"]

NUM_RE = re.compile(r"(?<![\d.,])(-?)(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(%?)")
CITE_GROUP_RE = re.compile(r"[（(]([^（）()]*?年报第\d+页[^（）()]*?)[）)]")


# ---------------------------------------------------------------- helpers
def strip_non_data(text: str) -> str:
    """Remove things that contain digits but are not data."""
    text = re.sub(r"(?m)^(#{1,6}\s*)\d+(\.\d+)+", r"\1", text)        # heading numbers "### 5.1"
    text = re.sub(r"(?m)^\s*\d+(\.\d+)*[.、)]\s", " ", text)          # list numbers "1. " "2、"
    text = re.sub(r"(?m)^\s*\d+(\.\d+)+\s", " ", text)                # "5.1 WACC推导" without #
    text = re.sub(r"\d{4}-\d{2}-\d{2}|\d{8}", " ", text)              # dates 2026-10-08 / 20260630
    text = re.sub(r"(?:20\d\d年报)?第\d+页", " ", text)                # page references
    text = re.sub(r"第\d+/\d+", " ", text)                            # ranks 第2/5
    text = re.sub(r"[a-zA-Z]{2}\d{6}|\b\d{6}\b", " ", text)            # stock codes
    return text


def extract_numbers(text: str) -> list[tuple[str, float, int]]:
    """(raw string, value, position) for every number that counts as data."""
    out = []
    for m in NUM_RE.finditer(text):
        sign, intpart, dec, pct = m.groups()
        raw = m.group(0)
        value = float(sign + intpart.replace(",", "") + (dec or ""))
        if not dec and not pct and not sign:
            v = int(value)
            if v <= 12 or 1990 <= v <= 2035:                            # small counts ("3年", "5家") and years
                continue
        out.append((raw, round(value, 4), m.start()))
    return out


def number_values(text: str) -> set[float]:
    return {v for _, v, _ in extract_numbers(strip_non_data(text))} | \
           {round(abs(v), 4) for _, v, _ in extract_numbers(strip_non_data(text))}


def citations(text: str) -> list[tuple[int, int]]:
    """All (year, page) citations. "（2024年报第22页、第15页）": 第15页 inherits 2024."""
    found = []
    for grp in CITE_GROUP_RE.findall(text):
        year = None
        for m in re.finditer(r"(20\d\d)年报|第(\d+)页", grp):
            if m.group(1):
                year = int(m.group(1))
            elif year:
                found.append((year, int(m.group(2))))
    return found


# ---------------------------------------------------------------- checks
def evaluate(report_path: Path) -> dict:
    report = report_path.read_text(encoding="utf-8")
    facts = json.loads((REPORTS / f"{TARGET}_facts.json").read_text(encoding="utf-8"))
    qa_path = REPORTS / f"{TARGET}_annual_report_qa.json"
    qa = json.loads(qa_path.read_text(encoding="utf-8")) if qa_path.exists() else []

    # 1. number traceability
    known = number_values(json.dumps(facts, ensure_ascii=False))
    clean = strip_non_data(report)
    nums = extract_numbers(clean)
    untraceable = []
    for raw, v, pos in nums:
        if v not in known and abs(v) not in known:
            untraceable.append({"number": raw, "context": clean[max(0, pos - 25): pos + 15].replace("\n", " ")})
    traced = len(nums) - len(untraceable)

    # 2. page citations
    valid_pages = set()
    for item in qa:
        for c in (item.get("llm") or {}).get("valid_citations", []):
            m = re.match(r"(\d{4})年报第(\d+)页", c)
            valid_pages.add((int(m.group(1)), int(m.group(2))))
    cites = citations(report)
    bad_cites = sorted({f"{y}年报第{p}页" for y, p in cites if (y, p) not in valid_pages})

    # 3. rating & fair-value range
    concl = facts["评级与结论(由规则计算,不得更改)"]
    stated = re.findall(r"评级[：:]\s*\**\s*(" + "|".join(RATINGS) + ")", report)
    rating_ok = bool(stated) and all(s == concl["评级"] for s in stated)
    low, high = [s.strip() for s in concl["合理价值区间(元)"].split("~")]
    range_ok = bool(re.search(rf"{re.escape(low)}\s*[~～-]\s*{re.escape(high)}", report))

    # 4. structure, 5. open items
    missing = [s for s in REQUIRED_SECTIONS if not re.search(rf"(?m)^#+\s*{s}", report)]
    open_items = report.count("待年报验证")

    return {
        "report": report_path.name,
        "numbers_total": len(nums), "numbers_traced": traced,
        "traceability": round(traced / len(nums), 4) if nums else None,
        "untraceable": untraceable,
        "page_citations_total": len(cites), "page_citations_invalid": bad_cites,
        "rating_expected": concl["评级"], "rating_stated": sorted(set(stated)), "rating_ok": rating_ok,
        "fair_value_range_expected": concl["合理价值区间(元)"], "range_ok": range_ok,
        "missing_sections": missing,
        "open_items_待年报验证": open_items,
        "passed": bool(not untraceable and not bad_cites and rating_ok and range_ok and not missing),
    }


def print_result(r: dict) -> None:
    ok = lambda b: "PASS" if b else "FAIL"  # noqa: E731
    print(f"\n=== {r['report']} ===")
    print(f"  Number traceability   {r['numbers_traced']}/{r['numbers_total']} = {r['traceability']:.1%}"
          f"   {ok(not r['untraceable'])}")
    for u in r["untraceable"][:15]:
        print(f"      untraceable: {u['number']:<12} ...{u['context']}...")
    if len(r["untraceable"]) > 15:
        print(f"      ... and {len(r['untraceable']) - 15} more (see json)")
    print(f"  Page citations        {r['page_citations_total']} cited, invalid {len(r['page_citations_invalid'])}"
          f"   {ok(not r['page_citations_invalid'])}  {r['page_citations_invalid'] or ''}")
    print(f"  Rating                expected {r['rating_expected']}, stated {r['rating_stated']}   {ok(r['rating_ok'])}")
    print(f"  Fair-value range      {r['fair_value_range_expected']}   {ok(r['range_ok'])}")
    print(f"  Sections              missing {r['missing_sections'] or 'none'}   {ok(not r['missing_sections'])}")
    print(f"  Open items            待年报验证 x {r['open_items_待年报验证']}")
    print(f"  OVERALL               {ok(r['passed'])}")


if __name__ == "__main__":
    paths = [Path(p) for p in sys.argv[1:]] or [REPORTS / f"{TARGET}_draft.md"]
    results = []
    for p in paths:
        p = p if p.is_absolute() else PROJECT_ROOT / p
        r = evaluate(p)
        results.append(r)
        (REPORTS / f"{TARGET}_eval_{p.stem}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2),
                                                              encoding="utf-8")
        print_result(r)
    if len(results) > 1:
        print("\nSummary")
        print(f"  {'report':<28}{'traceability':>13}{'untraceable':>13}{'citations':>11}{'invalid':>9}{'待验证':>8}")
        for r in results:
            print(f"  {r['report']:<28}{r['traceability']:>13.1%}{len(r['untraceable']):>13}"
                  f"{r['page_citations_total']:>11}{len(r['page_citations_invalid']):>9}{r['open_items_待年报验证']:>8}")
    print(f"\nSaved -> reports/{TARGET}_eval_<report>.json")