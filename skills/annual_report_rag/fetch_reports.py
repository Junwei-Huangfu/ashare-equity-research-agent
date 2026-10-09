"""Skill 5a: Annual-report RAG — download the target's full annual reports (PDF) from CNINFO (巨潮资讯).

CNINFO is the CSRC-designated disclosure platform. Verified reachable from Australia:
  - the list comes from AKShare (ak.stock_zh_a_disclosure_report_cninfo)
  - the PDF lives at http://static.cninfo.com.cn/finalpage/{announcement date}/{announcement id}.PDF

Output: data/raw/annual_reports/{code}_{year}.pdf     (git-ignored: large, and re-downloadable)

Usage (run from the project root):
    python skills/annual_report_rag/fetch_reports.py
"""
import re
import sys
import time
from pathlib import Path

import akshare as ak
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = PROJECT_ROOT / "data" / "raw" / "annual_reports"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]
YEARS = [2021, 2022, 2023, 2024, 2025]     # fiscal years to download
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def list_annual_reports(code: str) -> dict:
    """{fiscal year: pdf url} for FULL annual reports (no summaries, English versions or corrections)."""
    df = ak.stock_zh_a_disclosure_report_cninfo(symbol=code[2:], market="沪深京", category="年报",
                                               start_date="20200101", end_date="20991231")
    out = {}
    for _, row in df.iterrows():
        title = row["公告标题"]
        m = re.fullmatch(r".*?(\d{4})年年度报告", title)          # must END with 年年度报告
        if not m:
            continue
        year = int(m.group(1))
        aid = re.search(r"announcementId=(\d+)", row["公告链接"])
        adate = re.search(r"announcementTime=(\d{4}-\d{2}-\d{2})", row["公告链接"])
        if aid and adate and year not in out:                   # list is newest first -> keep the latest one
            out[year] = f"http://static.cninfo.com.cn/finalpage/{adate.group(1)}/{aid.group(1)}.PDF"
    return out


if __name__ == "__main__":
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    name = COMPANIES[TARGET]
    urls = list_annual_reports(TARGET)
    print(f"{name} ({TARGET}): annual reports found for {sorted(urls)}")
    for year in YEARS:
        path = PDF_DIR / f"{TARGET}_{year}.pdf"
        if path.exists():
            print(f"  Skip {year}: already downloaded")
            continue
        if year not in urls:
            print(f"  {year}: not found on CNINFO")
            continue
        print(f"  Downloading {year} annual report ...")
        resp = requests.get(urls[year], headers=HEADERS, timeout=120)
        resp.raise_for_status()
        if not resp.content.startswith(b"%PDF"):
            raise RuntimeError(f"{year}: downloaded file is not a PDF")
        path.write_bytes(resp.content)
        print(f"    Saved {len(resp.content)/1e6:.1f} MB -> {path.name}")
        time.sleep(1)
    print("Done.")