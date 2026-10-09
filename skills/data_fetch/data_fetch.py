"""Skill 1: Data collection — financial statements, market/valuation data and risk-free rate.

Sources (all verified to be reachable from Australia):
  - Financial statements : Sina Finance  (ak.stock_financial_report_sina)
  - Price / shares / mkt cap / PE / PB : East Money (ak.stock_value_em)
  - China 10Y government bond yield    : ak.bond_zh_us_rate

Usage (run from the project root):
    python skills/data_fetch/data_fetch.py                 # all companies, use cache
    python skills/data_fetch/data_fetch.py sz000538        # one stock only
    python skills/data_fetch/data_fetch.py --refresh       # re-download everything
"""
import sys
import time
from pathlib import Path

import akshare as ak
import pandas as pd

# This file lives in <project>/skills/data_fetch/, so go up 2 levels to reach the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Target company + comparable peers (TCM / pharma)
COMPANIES = {
    "sz000538": "云南白药",  # target
    "sh600436": "片仔癀",    # peer
    "sh600085": "同仁堂",    # peer
    "sh600332": "白云山",    # peer
}
STATEMENTS = ["资产负债表", "利润表", "现金流量表"]


def _save(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  Saved {len(df)} rows -> {path.name}")


def fetch_statements(code: str, refresh: bool = False) -> None:
    """Three financial statements for one stock (Sina)."""
    name = COMPANIES.get(code, code)
    for statement in STATEMENTS:
        path = RAW_DIR / f"{code}_{statement}.csv"
        if path.exists() and not refresh:
            print(f"  Skip {name} ({code}) - {statement}: already downloaded")
            continue
        print(f"Fetching {name} ({code}) - {statement} ...")
        _save(ak.stock_financial_report_sina(stock=code, symbol=statement), path)
        time.sleep(1)  # be polite to the data source


def fetch_market(code: str, refresh: bool = False) -> None:
    """Daily close, total shares, market cap, PE, PB for one stock (East Money).

    East Money wants the 6-digit code without the sh/sz prefix.
    """
    name = COMPANIES.get(code, code)
    path = RAW_DIR / f"{code}_估值行情.csv"
    if path.exists() and not refresh:
        print(f"  Skip {name} ({code}) - 估值行情: already downloaded")
        return
    print(f"Fetching {name} ({code}) - 估值行情 ...")
    _save(ak.stock_value_em(symbol=code[2:]), path)
    time.sleep(1)


def fetch_risk_free(refresh: bool = False) -> None:
    """China 10Y government bond yield (%), used as the risk-free rate in WACC."""
    path = RAW_DIR / "无风险利率_中国10年国债.csv"
    if path.exists() and not refresh:
        print("  Skip 无风险利率: already downloaded")
        return
    print("Fetching China 10Y government bond yield ...")
    df = ak.bond_zh_us_rate(start_date="20200101")
    # Keep only the China 10Y column and drop days with no China quote (holidays)
    df = df[["日期", "中国国债收益率10年"]].dropna()
    _save(df, path)


if __name__ == "__main__":
    args = sys.argv[1:]
    refresh = "--refresh" in args
    codes = [a for a in args if not a.startswith("--")] or list(COMPANIES)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for c in codes:
        fetch_statements(c, refresh)
        fetch_market(c, refresh)
    fetch_risk_free(refresh)
    print("Done.")