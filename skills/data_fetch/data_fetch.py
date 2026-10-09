"""Skill 1: Data collection — financial statements, D&A, market/valuation data and risk-free rate.

Sources (all verified to be reachable from Australia):
  - Financial statements : Sina Finance  (ak.stock_financial_report_sina)
  - Depreciation & amortisation (D&A) : East Money cash flow (ak.stock_cash_flow_sheet_by_report_em)
        Sina has no D&A. Cross-checked against Tonghuashun: totals match, only the
        right-of-use asset depreciation is classified differently.
  - Price / shares / mkt cap / PE / PB : East Money (ak.stock_value_em)
  - China 10Y government bond yield    : ak.bond_zh_us_rate
  - Daily prices, back-adjusted (后复权) : Sina (ak.stock_zh_a_daily, adjust="hfq")  -> for Beta
  - CSI 300 index (沪深300)             : Sina (ak.stock_zh_index_daily)            -> for Beta

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
    "sz000999": "华润三九",  # peer
}
STATEMENTS = ["资产负债表", "利润表", "现金流量表"]
PRICE_START = "20200101"  # price history start date (enough for a 3-year weekly Beta)

# East Money D&A columns we keep (yuan). Note: OILGAS_BIOLOGY_DEPR duplicates FA_IR_DEPR, so it is NOT kept.
DNA_COLUMNS = {
    "FA_IR_DEPR": "固定资产折旧",
    "USERIGHT_ASSET_AMORTIZE": "使用权资产折旧",
    "IA_AMORTIZE": "无形资产摊销",
    "LPE_AMORTIZE": "长期待摊费用摊销",
}


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


def fetch_dna(code: str, refresh: bool = False) -> None:
    """Depreciation & amortisation by report period (East Money cash-flow supplement).

    East Money wants the code as e.g. "SZ000538" (upper-case prefix).
    Output columns: 报告日 (YYYYMMDD, same format as Sina) + the four D&A items + 折旧摊销合计.
    """
    name = COMPANIES.get(code, code)
    path = RAW_DIR / f"{code}_折旧摊销.csv"
    if path.exists() and not refresh:
        print(f"  Skip {name} ({code}) - 折旧摊销: already downloaded")
        return
    print(f"Fetching {name} ({code}) - 折旧摊销 ...")
    raw = ak.stock_cash_flow_sheet_by_report_em(symbol=code.upper())
    df = pd.DataFrame({"报告日": pd.to_datetime(raw["REPORT_DATE"]).dt.strftime("%Y%m%d")})
    for en, cn in DNA_COLUMNS.items():
        df[cn] = pd.to_numeric(raw[en], errors="coerce") if en in raw.columns else float("nan")
    items = list(DNA_COLUMNS.values())
    df["折旧摊销合计"] = df[items].sum(axis=1, min_count=1)  # NaN if every item is missing
    _save(df, path)
    time.sleep(1)


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


def fetch_prices(code: str, refresh: bool = False) -> None:
    """Daily back-adjusted (后复权) prices, used to compute Beta.

    Back-adjusted prices include dividends and splits, so returns are not distorted
    on ex-dividend days.
    """
    name = COMPANIES.get(code, code)
    path = RAW_DIR / f"{code}_日线后复权.csv"
    if path.exists() and not refresh:
        print(f"  Skip {name} ({code}) - 日线后复权: already downloaded")
        return
    print(f"Fetching {name} ({code}) - 日线后复权 ...")
    df = ak.stock_zh_a_daily(symbol=code, start_date=PRICE_START, end_date="20991231", adjust="hfq")
    _save(df[["date", "close"]], path)
    time.sleep(1)


def fetch_index(refresh: bool = False) -> None:
    """CSI 300 index daily close (market proxy for Beta)."""
    path = RAW_DIR / "指数_沪深300.csv"
    if path.exists() and not refresh:
        print("  Skip 沪深300: already downloaded")
        return
    print("Fetching CSI 300 index ...")
    df = ak.stock_zh_index_daily(symbol="sh000300")
    df = df[pd.to_datetime(df["date"]) >= pd.Timestamp(PRICE_START)]
    _save(df[["date", "close"]], path)


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
        fetch_dna(c, refresh)
        fetch_market(c, refresh)
        fetch_prices(c, refresh)
    fetch_index(refresh)
    fetch_risk_free(refresh)
    print("Done.")