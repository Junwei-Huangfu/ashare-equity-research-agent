"""Orchestrator: run every skill in order, from raw data to the reviewed final report.

  1 data_fetch            statements, D&A, market data, prices, risk-free rate
  2 financial_analysis    profitability, growth, DuPont, cash flow, peers
  3 valuation             WACC -> DCF -> comparable companies + valuation summary
  4 fraud_risk            Beneish M-Score (5 & 8 variables) + China red flags, with driver attribution
  5 annual_report_rag     download annual reports -> chunk + BM25 index -> cited Q&A
  6 report_writer         facts pack -> draft report (LLM writes, Python computes)
  7 evaluation            rule-based checks of the draft
  8 review                reviewer agent (thinking) -> reviser agent -> final report
  9 evaluation            rule-based checks of the final report
 10 review --verify       (optional) reviewer checks the final report again

Each skill is an independent script with its own SKILL.md; this file only decides the order.
Stops at the first failing step.

Usage (run from the project root):
    python run_pipeline.py              # full run (LLM steps cost a few cents)
    python run_pipeline.py --offline    # no LLM calls, no cost: data, analysis, valuation, risk, annual-report index
    python run_pipeline.py --verify     # full run + second review of the final report
    python run_pipeline.py --from 6     # start from step 6 (reuse the outputs of steps 1-5)
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S = "skills"

sys.path.insert(0, str(ROOT / S / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]

offline = "--offline" in sys.argv
verify = "--verify" in sys.argv
start = int(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 1

# (step, name, command, needs_llm)
STEPS = [
    (1, "Data collection", [f"{S}/data_fetch/data_fetch.py"], False),
    (2, "Financial analysis", [f"{S}/financial_analysis/financial_analysis.py"], False),
    (3, "Valuation: WACC", [f"{S}/valuation/wacc.py"], False),
    (3, "Valuation: DCF", [f"{S}/valuation/dcf.py"], False),
    (3, "Valuation: comparable companies", [f"{S}/valuation/comps.py"], False),
    (4, "Fraud-risk screening", [f"{S}/fraud_risk/ratios.py"], False),
    (5, "Annual reports: download", [f"{S}/annual_report_rag/fetch_reports.py"], False),
    (5, "Annual reports: index", [f"{S}/annual_report_rag/index.py"], False),
    (5, "Annual reports: Q&A", [f"{S}/annual_report_rag/qa.py"], True),
    (6, "Report writer", [f"{S}/report_writer/writer.py"], True),
    (7, "Evaluate draft", [f"{S}/evaluation/evaluate.py"], False),
    (8, "Review + revise", [f"{S}/report_writer/review.py"], True),
    (9, "Evaluate final", [f"{S}/evaluation/evaluate.py", f"reports/{TARGET}_final.md"], False),
    (10, "Review final (verify)", [f"{S}/report_writer/review.py", "--verify"], True),
]

if __name__ == "__main__":
    t_all = time.time()
    for n, name, cmd, needs_llm in STEPS:
        if n < start or (n == 10 and not verify):
            continue
        if offline and (needs_llm or n >= 7):
            print(f"\n[{n}] {name}: skipped (--offline)")
            continue
        print(f"\n{'=' * 70}\n[{n}] {name}\n{'=' * 70}", flush=True)
        t0 = time.time()
        result = subprocess.run([sys.executable, *cmd], cwd=ROOT)
        if result.returncode != 0:
            print(f"\nStep [{n}] {name} FAILED (exit code {result.returncode}). Pipeline stopped.")
            sys.exit(result.returncode)
        print(f"--- [{n}] {name} done in {time.time() - t0:.1f}s")
    print(f"\nPipeline finished in {time.time() - t_all:.1f}s"
          + ("" if offline else f". Final report: reports/{TARGET}_final.md"))