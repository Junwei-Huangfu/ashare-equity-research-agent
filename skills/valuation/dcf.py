"""Skill 3b: Valuation — FCFF discounted cash flow with sensitivity analysis.

Input : config/valuation.toml          (all human assumptions)
        data/processed/wacc.json       (from wacc.py — run that first)
        data/raw/{code}_利润表.csv / 资产负债表.csv / 现金流量表.csv / 折旧摊销.csv / 估值行情.csv
Output: data/processed/dcf.json              (key results + every assumption actually used)
        data/processed/dcf_forecast.csv      (2026E-2030E forecast table)
        data/processed/dcf_sensitivity.csv   (value per share: WACC x terminal growth)

FCFF = EBIT x (1 - tax) + D&A - capex - delta NWC
Timing: cash flows are valued at the latest published balance-sheet date (2026-06-30), so
        2026E only contributes its second half, and the cash already earned in H1 is in the balance sheet.

Usage (run from the project root):
    python skills/valuation/wacc.py     # first
    python skills/valuation/dcf.py
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

YI = 1e8  # 1 亿 = 100 million yuan


# ---------------------------------------------------------------- data helpers
def read(code: str, name: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / f"{code}_{name}.csv", dtype={"报告日": str})
    num = [c for c in df.columns if c not in ("报告日", "公告日期", "数据源", "是否审计", "币种", "类型", "更新日期")]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")
    return df


def annual(df: pd.DataFrame) -> pd.DataFrame:
    """Keep 12-31 reports, index by fiscal year (int), ascending."""
    a = df[df["报告日"].str.endswith("1231")].copy()
    a.index = a["报告日"].str[:4].astype(int)
    return a.sort_index()


def first(df: pd.DataFrame, combined: str, *parts: str) -> pd.Series:
    """Use the combined line if present, otherwise the sum of its parts (Sina splits/merges lines across years)."""
    out = df[combined] if combined in df.columns else pd.Series(float("nan"), index=df.index)
    if parts:
        alt = sum(df[p].fillna(0) for p in parts if p in df.columns)
        out = out.fillna(alt)
    return out


def g(df: pd.DataFrame, c: str) -> pd.Series:
    """Column or zeros (an item that does not exist = 0)."""
    return df[c].fillna(0) if c in df.columns else pd.Series(0.0, index=df.index)


def resolve(value, auto_value: float) -> float:
    """Config value can be a number or an 'auto' keyword such as 'avg3' -> use the computed history."""
    return float(value) if isinstance(value, (int, float)) else float(auto_value)


# ---------------------------------------------------------------- history
def history(code: str) -> pd.DataFrame:
    inc, bs = annual(read(code, "利润表")), annual(read(code, "资产负债表"))
    cf, dna = annual(read(code, "现金流量表")), annual(read(code, "折旧摊销"))

    h = pd.DataFrame(index=inc.index)
    h["revenue"] = inc["营业收入"]
    h["core_ebit"] = (inc["营业收入"] - inc["营业成本"] - g(inc, "营业税金及附加")
                      - g(inc, "销售费用") - g(inc, "管理费用") - g(inc, "研发费用"))
    h["ebit_margin"] = h["core_ebit"] / h["revenue"]
    h["tax_rate"] = inc["所得税费用"] / inc["利润总额"]
    h["da_pct"] = dna["折旧摊销合计"].reindex(h.index) / h["revenue"]
    h["capex_pct"] = cf["购建固定资产、无形资产和其他长期资产所支付的现金"].reindex(h.index) / h["revenue"]

    b = bs.reindex(h.index)
    nwc_assets = (first(b, "应收票据及应收账款", "应收票据", "应收账款") + g(b, "应收款项融资")
                  + g(b, "预付款项") + g(b, "存货") + g(b, "合同资产"))
    nwc_liabs = (first(b, "应付票据及应付账款", "应付票据", "应付账款") + g(b, "预收款项")
                 + g(b, "合同负债") + g(b, "应付职工薪酬") + g(b, "应交税费"))
    h["nwc_pct"] = (nwc_assets - nwc_liabs) / h["revenue"]
    return h


def h1_yoy(code: str, latest_year: int) -> tuple[float, str]:
    inc = read(code, "利润表").set_index("报告日")
    this, last = f"{latest_year + 1}0630", f"{latest_year}0630"
    return inc.loc[this, "营业收入"] / inc.loc[last, "营业收入"] - 1, this


def latest_published_bs(code: str, end: pd.Timestamp) -> pd.Series:
    """Latest balance sheet already published on the valuation date (no look-ahead)."""
    bs = read(code, "资产负债表")
    known = pd.to_datetime(bs.get("公告日期"), errors="coerce").fillna(pd.to_datetime(bs["报告日"]))
    return bs[known <= end].sort_values("报告日").iloc[-1]


def market_row(code: str, end: pd.Timestamp) -> pd.Series:
    df = pd.read_csv(RAW_DIR / f"{code}_估值行情.csv", parse_dates=["数据日期"]).sort_values("数据日期")
    return df[df["数据日期"] <= end].iloc[-1]


# ---------------------------------------------------------------- DCF engine
def run_dcf(base_revenue, growth, margins, tax, da, capex, nwc, wacc, g_term, first_fraction):
    """Pure function: returns (forecast table, enterprise value). Used for base case AND sensitivity."""
    rows, rev_prev = [], base_revenue
    for i, (gr, m) in enumerate(zip(growth, margins)):
        rev = rev_prev * (1 + gr)
        ebit = rev * m
        fcff = ebit * (1 - tax) + rev * da - rev * capex - nwc * (rev - rev_prev)
        frac = first_fraction if i == 0 else 1.0           # 2026E: only the part after the base date
        t = first_fraction + i                               # years from base date to the END of this period
        df = 1 / (1 + wacc) ** t
        rows.append({"revenue": rev, "growth": gr, "ebit_margin": m, "ebit": ebit, "nopat": ebit * (1 - tax),
                     "da": rev * da, "capex": rev * capex, "delta_nwc": nwc * (rev - rev_prev),
                     "fcff": fcff, "fraction": frac, "t": t, "discount_factor": df, "pv_fcff": fcff * frac * df})
        rev_prev = rev
    table = pd.DataFrame(rows)
    last = table.iloc[-1]
    tv = last["fcff"] * (1 + g_term) / (wacc - g_term)
    pv_tv = tv * last["discount_factor"]
    ev = table["pv_fcff"].sum() + pv_tv
    return table, ev, tv, pv_tv


if __name__ == "__main__":
    cfg = tomllib.load(open(CONFIG, "rb"))
    target = cfg["general"]["target"]
    end = pd.Timestamp(cfg["general"]["valuation_date"])
    d, br = cfg["dcf"], cfg["bridge"]
    wacc = json.loads((OUT_DIR / "wacc.json").read_text(encoding="utf-8"))["wacc"]

    # ---- 1. history -> assumptions
    h = history(target)
    base_year = int(h.index[-1])
    last3, last5 = h.tail(3), h.tail(5)
    yoy, h1_date = h1_yoy(target, base_year)

    n = d["forecast_years"]
    g_term = d["terminal_growth"]
    g1 = resolve(d["first_year_growth"], yoy)
    growth = [g1 + (g_term - g1) * i / (n - 1) for i in range(n)]           # straight line to terminal
    m0, m_end = h["ebit_margin"].iloc[-1], resolve(d["ebit_margin_end"], last5["ebit_margin"].mean())
    margins = [m0 + (m_end - m0) * (i + 1) / n for i in range(n)]           # fade from latest to target
    tax = resolve(d["tax_rate"], last3["tax_rate"].mean())
    da = resolve(d["da_pct_revenue"], last3["da_pct"].mean())
    capex = resolve(d["capex_pct_revenue"], last3["capex_pct"].mean())
    nwc = resolve(d["nwc_pct_revenue"], last3["nwc_pct"].mean())

    # ---- 2. timing: value at the latest published balance-sheet date
    bs = latest_published_bs(target, end)
    base_date = pd.Timestamp(bs["报告日"])
    year_end = pd.Timestamp(f"{base_year + 1}-12-31")
    first_fraction = (year_end - base_date).days / 365                       # e.g. 0.5 from 06-30

    # ---- 3. DCF
    table, ev, tv, pv_tv = run_dcf(h["revenue"].iloc[-1], growth, margins, tax, da, capex, nwc,
                                   wacc, g_term, first_fraction)
    table.index = [f"{base_year + i + 1}E" for i in range(n)]

    # ---- 4. EV -> equity bridge
    revenue_last = h["revenue"].iloc[-1]
    cash = bs.get("货币资金", 0) or 0
    operating_cash = br["operating_cash_pct_revenue"] * revenue_last
    excess_cash = max(cash - operating_cash, 0)
    non_op = {k: float(bs.get(k)) for k in br["add_non_operating"] if pd.notna(bs.get(k))}
    debt = {k: float(bs.get(k)) for k in br["subtract_debt"] if pd.notna(bs.get(k))}
    minority = float(bs.get(br["subtract_minority"]) or 0)
    equity = ev + excess_cash + sum(non_op.values()) - sum(debt.values()) - minority

    mk = market_row(target, end)
    shares, price = float(mk["总股本"]), float(mk["当日收盘价"])
    per_share = equity / shares
    upside = per_share / price - 1

    # ---- 5. sensitivity: WACC x terminal growth (everything else fixed)
    s = cfg["sensitivity"]
    bridge_net = excess_cash + sum(non_op.values()) - sum(debt.values()) - minority
    sens = pd.DataFrame(index=[f"{w:.1%}" for w in s["wacc"]], columns=[f"{x:.2%}" for x in s["terminal_growth"]])
    for w in s["wacc"]:
        for x in s["terminal_growth"]:
            gr = [g1 + (x - g1) * i / (n - 1) for i in range(n)]
            _, ev_s, _, _ = run_dcf(revenue_last, gr, margins, tax, da, capex, nwc, w, x, first_fraction)
            sens.loc[f"{w:.1%}", f"{x:.2%}"] = round((ev_s + bridge_net) / shares, 2)
    sens.index.name = "WACC \\ g"

    # ---- 6. save
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_tbl = table.copy()
    for c in ["revenue", "ebit", "nopat", "da", "capex", "delta_nwc", "fcff", "pv_fcff"]:
        out_tbl[c] = out_tbl[c] / YI
    out_tbl.round(4).to_csv(OUT_DIR / "dcf_forecast.csv", encoding="utf-8-sig")
    sens.to_csv(OUT_DIR / "dcf_sensitivity.csv", encoding="utf-8-sig")
    result = {
        "target": target, "name": COMPANIES[target], "valuation_date": str(end.date()),
        "base_date": str(base_date.date()), "base_year": base_year, "first_period_fraction": round(first_fraction, 4),
        "assumptions": {
            "wacc": wacc, "terminal_growth": g_term,
            "first_year_growth": round(g1, 4), "first_year_growth_source": f"{h1_date} revenue YoY",
            "growth_path": [round(x, 4) for x in growth],
            "ebit_margin_latest": round(m0, 4), "ebit_margin_end": round(m_end, 4),
            "ebit_margin_path": [round(x, 4) for x in margins],
            "tax_rate": round(tax, 4), "da_pct_revenue": round(da, 4),
            "capex_pct_revenue": round(capex, 4), "nwc_pct_revenue": round(nwc, 4),
        },
        "history": h.round(4).reset_index(names="year").to_dict(orient="records"),
        "enterprise_value_yi": round(ev / YI, 2),
        "pv_explicit_fcff_yi": round(table["pv_fcff"].sum() / YI, 2),
        "terminal_value_yi": round(tv / YI, 2), "pv_terminal_value_yi": round(pv_tv / YI, 2),
        "terminal_value_share_of_ev": round(pv_tv / ev, 4),
        "bridge_yi": {
            "货币资金": round(cash / YI, 2),
            "减:经营性现金(营收x比例)": round(operating_cash / YI, 2),
            "+超额现金": round(excess_cash / YI, 2),
            **{f"+{k}": round(v / YI, 2) for k, v in non_op.items()},
            **{f"-{k}": round(v / YI, 2) for k, v in debt.items()},
            "-少数股东权益": round(minority / YI, 2),
        },
        "equity_value_yi": round(equity / YI, 2),
        "shares_yi": round(shares / YI, 4), "value_per_share": round(per_share, 2),
        "price": price, "price_date": str(mk["数据日期"].date()), "upside": round(upside, 4),
    }
    (OUT_DIR / "dcf.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- 7. print
    a = result["assumptions"]
    print(f"{COMPANIES[target]} DCF (FCFF)   base date {base_date.date()}   WACC {wacc:.2%}   g {g_term:.1%}")
    print("\nAssumptions derived from history")
    print(f"  2026E growth (H1 YoY)        {g1:.2%}  -> path {', '.join(f'{x:.2%}' for x in growth)}")
    print(f"  Core EBIT margin             {m0:.2%} (latest) -> {m_end:.2%} (5y avg) by {base_year + n}E")
    print(f"  Effective tax rate (3y avg)  {tax:.2%}")
    print(f"  D&A / capex / NWC (% rev)    {da:.2%} / {capex:.2%} / {nwc:.2%}")
    show = out_tbl[["revenue", "growth", "ebit_margin", "nopat", "da", "capex", "delta_nwc", "fcff", "fraction", "pv_fcff"]].T
    pct_rows = ["growth", "ebit_margin"]
    show = show.apply(lambda col: [f"{v:.2%}" if r in pct_rows else f"{v:,.2f}" for r, v in col.items()])
    print("\nForecast (亿元; growth & margin in %)")
    print(show.to_string())
    print(f"\n  PV of explicit FCFF          {table['pv_fcff'].sum()/YI:>9,.2f} 亿")
    print(f"  PV of terminal value         {pv_tv/YI:>9,.2f} 亿  ({pv_tv/ev:.0%} of EV)")
    print(f"  Enterprise value             {ev/YI:>9,.2f} 亿")
    for k, v in result["bridge_yi"].items():
        print(f"    {k:<26}{v:>9,.2f}")
    print(f"  Equity value                 {equity/YI:>9,.2f} 亿")
    print(f"  Shares                       {shares/YI:>9,.2f} 亿")
    print(f"  Value per share              {per_share:>9,.2f} 元   vs price {price:.2f} ({mk['数据日期'].date()})  -> {upside:+.1%}")
    print("\nSensitivity: value per share (元), rows = WACC, columns = terminal growth")
    print(sens.astype(float).to_string(float_format=lambda v: f"{v:.2f}"))
    print("\nSaved -> data/processed/dcf.json, dcf_forecast.csv, dcf_sensitivity.csv")