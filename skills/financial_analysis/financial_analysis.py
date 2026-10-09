"""Skill 2: Financial analysis — profitability, growth, DuPont, cash-flow quality, balance sheet, efficiency.

Input : data/raw/{code}_利润表.csv / 资产负债表.csv / 现金流量表.csv   (from Skill 1)
Output: data/processed/{code}_financial_analysis.csv   (rows = metrics, columns = years)
        data/processed/peer_comparison.csv             (latest year, all companies side by side)

Principle: every number is calculated by Python from the raw statements; the LLM never does arithmetic.

Usage (run from the project root):
    python skills/financial_analysis/financial_analysis.py
"""
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUT_DIR = PROJECT_ROOT / "data" / "processed"

# Reuse the company list from Skill 1 so there is only one place to edit it
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

N_YEARS = 5  # number of fiscal years to report


# ---------------------------------------------------------------- loading
def load_annual(code: str) -> pd.DataFrame:
    """Merge the three statements and keep annual reports (报告日 ending 1231) only.

    Returns one row per fiscal year (ascending), all values numeric (yuan).
    """
    merged = None
    for st in ["利润表", "资产负债表", "现金流量表"]:
        df = pd.read_csv(RAW_DIR / f"{code}_{st}.csv", dtype={"报告日": str})
        df = df[df["报告日"].str.endswith("1231")].copy()
        df["年度"] = df["报告日"].str[:4].astype(int)
        df = df.drop(columns=["报告日"]).set_index("年度")
        if merged is None:
            merged = df
        else:
            new_cols = [c for c in df.columns if c not in merged.columns]
            merged = merged.join(df[new_cols], how="outer")
    merged = merged.apply(pd.to_numeric, errors="coerce")
    return merged.sort_index()


def col(df: pd.DataFrame, *names: str) -> pd.Series:
    """Return the first column that has data; later names are fallbacks.

    e.g. col(df, "应收账款", "应收票据及应收账款") — in 2018-2019 Sina merged these two.
    Missing columns / missing values are treated as 0 only after all fallbacks fail.
    """
    out = pd.Series(float("nan"), index=df.index)
    for n in names:
        if n in df.columns:
            out = out.fillna(df[n])
    return out


def avg(s: pd.Series) -> pd.Series:
    """Average of opening and closing balance (opening = previous year's closing)."""
    return (s + s.shift(1)) / 2


# ---------------------------------------------------------------- metrics
def analyse(code: str) -> pd.DataFrame:
    d = load_annual(code)
    z = lambda *names: col(d, *names).fillna(0)  # noqa: E731  (missing item = 0, e.g. no bonds issued)

    revenue = col(d, "营业收入")
    cogs = col(d, "营业成本")
    net_profit = col(d, "净利润")
    np_parent = col(d, "归属于母公司所有者的净利润")
    total_assets = col(d, "资产总计")
    equity_total = col(d, "所有者权益(或股东权益)合计")
    equity_parent = col(d, "归属于母公司股东权益合计")
    cfo = col(d, "经营活动产生的现金流量净额")
    capex = z("购建固定资产、无形资产和其他长期资产所支付的现金")
    receivables = col(d, "应收账款", "应收票据及应收账款")
    inventory = col(d, "存货")
    cash = z("货币资金")
    interest_debt = z("短期借款") + z("长期借款") + z("应付债券") + z("一年内到期的非流动负债")

    m = pd.DataFrame(index=d.index)

    # 1. Profitability
    m["营业收入(亿元)"] = revenue / 1e8
    m["归母净利润(亿元)"] = np_parent / 1e8
    m["毛利率"] = (revenue - cogs) / revenue
    m["销售费用率"] = z("销售费用") / revenue
    m["管理费用率"] = z("管理费用") / revenue
    m["研发费用率"] = z("研发费用") / revenue
    m["财务费用率"] = z("财务费用") / revenue
    m["净利率"] = net_profit / revenue
    m["ROE(归母,平均)"] = np_parent / avg(equity_parent)
    m["ROA(平均)"] = net_profit / avg(total_assets)

    # 2. Growth
    m["营收增速"] = revenue.pct_change(fill_method=None)
    m["归母净利润增速"] = np_parent.pct_change(fill_method=None)

    # 3. DuPont (3-factor, on total equity so the identity holds exactly)
    m["杜邦_净利率"] = net_profit / revenue
    m["杜邦_总资产周转率"] = revenue / avg(total_assets)
    m["杜邦_权益乘数"] = avg(total_assets) / avg(equity_total)
    m["杜邦_ROE(全部权益)"] = m["杜邦_净利率"] * m["杜邦_总资产周转率"] * m["杜邦_权益乘数"]

    # 4. Cash-flow quality
    m["经营现金流(亿元)"] = cfo / 1e8
    m["经营现金流/净利润"] = cfo / net_profit
    m["收现比"] = z("销售商品、提供劳务收到的现金") / revenue
    m["资本开支(亿元)"] = capex / 1e8
    m["资本开支/营收"] = capex / revenue
    m["自由现金流(亿元)"] = (cfo - capex) / 1e8   # simple FCF = CFO - capex

    # 5. Balance sheet / solvency
    m["资产负债率"] = z("负债合计") / total_assets
    m["有息负债(亿元)"] = interest_debt / 1e8
    m["净现金(亿元)"] = (cash - interest_debt) / 1e8

    # 6. Efficiency
    m["应收账款周转天数"] = avg(receivables) / revenue * 365
    m["存货周转天数"] = avg(inventory) / cogs * 365

    # Keep the latest N fiscal years (earlier years were only needed for averages / growth)
    m = m.tail(N_YEARS)
    return m.T.round(4)  # rows = metrics, columns = years


# ---------------------------------------------------------------- main
def fmt(v, metric):
    """Pretty print: amounts / days as numbers, ratios as percentages."""
    if pd.isna(v):
        return "-"
    if "亿元" in metric or "天数" in metric or metric in ("杜邦_总资产周转率", "杜邦_权益乘数",
                                                         "经营现金流/净利润", "收现比"):
        return f"{v:,.2f}"
    return f"{v:.1%}"


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    latest = {}
    for code, name in COMPANIES.items():
        table = analyse(code)
        path = OUT_DIR / f"{code}_financial_analysis.csv"
        table.to_csv(path, encoding="utf-8-sig")
        print(f"Saved {name} ({code}) -> {path.name}  years: {list(table.columns)}")
        latest[f"{name}"] = table[table.columns[-1]]
        latest_year = table.columns[-1]

    peers = pd.DataFrame(latest)
    peers.to_csv(OUT_DIR / "peer_comparison.csv", encoding="utf-8-sig")
    print(f"Saved peer comparison ({latest_year}) -> peer_comparison.csv\n")

    # Print the target company's table for a quick sanity check
    target = list(COMPANIES)[0]
    t = pd.read_csv(OUT_DIR / f"{target}_financial_analysis.csv", index_col=0)
    print(f"{COMPANIES[target]} ({target})")
    print(t.apply(lambda row: [fmt(v, row.name) for v in row], axis=1, result_type="expand")
           .set_axis(t.columns, axis=1).to_string())