"""Skill 3a: Valuation — Beta regression and WACC (CAPM).

Input : config/valuation.toml                       (human assumptions)
        data/raw/{code}_日线后复权.csv, 指数_沪深300.csv  (prices for Beta)
        data/raw/无风险利率_中国10年国债.csv            (risk-free rate)
        data/raw/{code}_估值行情.csv, {code}_资产负债表.csv (weights: market cap, debt)
Output: data/processed/wacc.json

Cost of equity = Rf + Beta x ERP          (CAPM)
WACC           = E/(D+E) x Ke + D/(D+E) x Kd x (1 - t)

Usage (run from the project root):
    python skills/valuation/wacc.py
"""
import json
import sys
import tomllib
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUT_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG = PROJECT_ROOT / "config" / "valuation.toml"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

DEBT_ITEMS = ["短期借款", "一年内到期的非流动负债", "长期借款", "应付债券", "租赁负债"]


def load_config() -> dict:
    with open(CONFIG, "rb") as f:
        return tomllib.load(f)


def weekly_returns(path: Path, end: pd.Timestamp, years: int, freq: str) -> pd.Series:
    """Daily close -> weekly simple returns inside the look-back window."""
    df = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
    df = df.loc[end - pd.DateOffset(years=years): end, "close"]
    return df.resample(freq).last().pct_change().dropna()


def regress_beta(code: str, cfg: dict, end: pd.Timestamp) -> dict:
    """OLS slope of stock weekly returns on CSI 300 weekly returns."""
    w = cfg["wacc"]
    stock = weekly_returns(RAW_DIR / f"{code}_日线后复权.csv", end, w["beta_lookback_years"], w["beta_frequency"])
    market = weekly_returns(RAW_DIR / "指数_沪深300.csv", end, w["beta_lookback_years"], w["beta_frequency"])
    both = pd.concat([stock, market], axis=1, keys=["s", "m"]).dropna()
    raw_beta = both["s"].cov(both["m"]) / both["m"].var()
    r2 = both["s"].corr(both["m"]) ** 2
    adj_beta = 0.67 * raw_beta + 0.33 if w["beta_blume_adjust"] else raw_beta
    return {"raw_beta": round(raw_beta, 4), "adjusted_beta": round(adj_beta, 4),
            "r_squared": round(r2, 4), "n_weeks": int(len(both)),
            "window": f"{both.index[0].date()} ~ {both.index[-1].date()}"}


def risk_free(end: pd.Timestamp) -> tuple[float, str]:
    """Latest China 10Y yield on or before the valuation date (decimal)."""
    df = pd.read_csv(RAW_DIR / "无风险利率_中国10年国债.csv", parse_dates=["日期"]).sort_values("日期")
    row = df[df["日期"] <= end].iloc[-1]
    return row["中国国债收益率10年"] / 100, str(row["日期"].date())


def market_cap(code: str, end: pd.Timestamp) -> tuple[float, str]:
    df = pd.read_csv(RAW_DIR / f"{code}_估值行情.csv", parse_dates=["数据日期"]).sort_values("数据日期")
    row = df[df["数据日期"] <= end].iloc[-1]
    return float(row["总市值"]), str(row["数据日期"].date())


def interest_bearing_debt(code: str, end: pd.Timestamp) -> tuple[float, str]:
    """Latest balance sheet already PUBLISHED on the valuation date (no look-ahead).

    Uses Sina's 公告日期 (announcement date); falls back to the period end if it is missing.
    """
    bs = pd.read_csv(RAW_DIR / f"{code}_资产负债表.csv", dtype={"报告日": str})
    known = pd.to_datetime(bs.get("公告日期"), errors="coerce").fillna(pd.to_datetime(bs["报告日"]))
    bs = bs[known <= end].sort_values("报告日")
    row = bs.iloc[-1]
    debt = sum(pd.to_numeric(row.get(i), errors="coerce") for i in DEBT_ITEMS
               if pd.notna(pd.to_numeric(row.get(i), errors="coerce")))
    return float(debt), row["报告日"]


if __name__ == "__main__":
    cfg = load_config()
    target = cfg["general"]["target"]
    end = pd.Timestamp(cfg["general"]["valuation_date"])
    w = cfg["wacc"]

    # Beta for every company (peers are shown for reference only)
    betas = {code: regress_beta(code, cfg, end) for code in COMPANIES}
    print("Beta vs CSI 300 (weekly, back-adjusted prices)")
    print(f"  {'公司':<6}{'raw':>8}{'adjusted':>10}{'R²':>8}{'weeks':>7}")
    for code, b in betas.items():
        print(f"  {COMPANIES[code]:<6}{b['raw_beta']:>8.2f}{b['adjusted_beta']:>10.2f}"
              f"{b['r_squared']:>8.2f}{b['n_weeks']:>7}")

    rf, rf_date = risk_free(end)
    beta = betas[target]["adjusted_beta"]
    ke = rf + beta * w["equity_risk_premium"]

    E, e_date = market_cap(target, end)
    D, d_date = interest_bearing_debt(target, end)
    kd_after_tax = w["pre_tax_cost_of_debt"] * (1 - w["tax_rate"])
    wacc = E / (D + E) * ke + D / (D + E) * kd_after_tax

    result = {
        "target": target, "name": COMPANIES[target], "valuation_date": str(end.date()),
        "risk_free_rate": round(rf, 6), "risk_free_date": rf_date,
        "beta": betas[target], "equity_risk_premium": w["equity_risk_premium"],
        "cost_of_equity": round(ke, 6),
        "market_cap": E, "market_cap_date": e_date,
        "interest_bearing_debt": D, "debt_report_date": d_date,
        "weight_equity": round(E / (D + E), 6), "weight_debt": round(D / (D + E), 6),
        "pre_tax_cost_of_debt": w["pre_tax_cost_of_debt"], "after_tax_cost_of_debt": round(kd_after_tax, 6),
        "wacc": round(wacc, 6),
        "peer_betas": {COMPANIES[c]: b for c, b in betas.items() if c != target},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "wacc.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{COMPANIES[target]} WACC (valuation date {end.date()})")
    print(f"  Risk-free rate (10Y CGB, {rf_date})   {rf:.2%}")
    print(f"  Adjusted Beta                         {beta:.2f}")
    print(f"  Equity risk premium                   {w['equity_risk_premium']:.2%}")
    print(f"  Cost of equity  Ke                    {ke:.2%}")
    print(f"  Market cap E ({e_date})          {E/1e8:,.1f} 亿")
    print(f"  Interest-bearing debt D ({d_date})   {D/1e8:,.2f} 亿")
    print(f"  Weights  E / D                        {E/(D+E):.2%} / {D/(D+E):.2%}")
    print(f"  After-tax cost of debt                {kd_after_tax:.2%}")
    print(f"  WACC                                  {wacc:.2%}")
    print("\nSaved -> data/processed/wacc.json")