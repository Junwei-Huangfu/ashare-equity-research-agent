"""Skill 4: Fraud-risk screening — reused from project 1 (ashare-fraud-risk-skill), upgraded.

Reused unchanged: the 5-variable Beneish M-Score and the China-specific red-flag rules
(存贷双高, cash-rich yet high financial cost, weak 3-year cash conversion, inventory outpacing revenue).
Upgraded: project 1 lacked depreciation, so only the 5-variable model was possible. This project
fetches D&A from East Money, so the full 8-variable Beneish model is now computed as well.

  M5 = -6.065 + 0.823 DSRI + 0.906 GMI + 0.593 AQI + 0.717 SGI + 7.770 TATA              (flag if > -2.22)
  M8 = -4.84 + 0.920 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI
       - 0.172 SGAI + 4.679 TATA - 0.327 LVGI                                             (flag if > -1.78)

Input : data/raw/{code}_资产负债表.csv / 利润表.csv / 现金流量表.csv / 折旧摊销.csv   (Skill 1)
Output: data/processed/{code}_fraud_risk.csv   (indicators + red flags by year, every company)
        data/processed/fraud_risk.json         (target company summary for the report writer)

Usage (run from the project root):
    python skills/fraud_risk/ratios.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUT_DIR = PROJECT_ROOT / "data" / "processed"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]
M5_THRESHOLD = -2.22
M8_THRESHOLD = -1.78
N_YEARS = 5

# Coefficients, used to explain WHICH variable pushed a score up
M5_COEF = {"DSRI": 0.823, "GMI": 0.906, "AQI": 0.593, "SGI": 0.717, "TATA": 7.770}
M8_COEF = {"DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115,
           "SGAI": -0.172, "TATA": 4.679, "LVGI": -0.327}
VAR_MEANING = {
    "DSRI": "应收账款周转指数：应收账款/营收 较上年的变化，>1 表示回款变慢",
    "GMI": "毛利率指数：上年毛利率/本年毛利率，>1 表示毛利率下滑",
    "AQI": "资产质量指数：除流动资产和固定资产以外的'软资产'占总资产比例的变化，>1 表示软资产占比上升",
    "SGI": "营收增长指数：本年营收/上年营收",
    "TATA": "总应计：(净利润-经营现金流)/总资产，越高表示利润中现金含量越低",
    "DEPI": "折旧率指数：上年折旧率/本年折旧率，>1 表示折旧放缓",
    "SGAI": "销管费用指数：销管费用/营收 较上年的变化",
    "LVGI": "杠杆指数：负债/总资产 较上年的变化",
}


def load_annual(code: str) -> pd.DataFrame:
    """Merge the three statements + D&A into one table of annual (Dec 31) reports."""
    frames = []
    for name in ["资产负债表", "利润表", "现金流量表", "折旧摊销"]:
        df = pd.read_csv(RAW_DIR / f"{code}_{name}.csv", dtype={"报告日": str})
        df = df[df["报告日"].str.endswith("1231")].set_index("报告日")
        frames.append(df)
    merged = frames[0].join(frames[1], rsuffix="_is").join(frames[2], rsuffix="_cf").join(frames[3], rsuffix="_da")
    merged.index = merged.index.str[:4].astype(int)
    return merged.sort_index()


def col(df: pd.DataFrame, *names: str) -> pd.Series:
    """Return the first available column, filling gaps with later fallbacks
    (e.g. 2018-19 reports merged receivables with notes receivable)."""
    result = pd.Series(np.nan, index=df.index)
    for n in names:
        if n in df.columns:
            result = result.fillna(pd.to_numeric(df[n], errors="coerce"))
    return result


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    sales = col(df, "营业收入", "营业总收入")
    cogs = col(df, "营业成本")
    ar = col(df, "应收账款", "应收票据及应收账款")
    ca = col(df, "流动资产合计")
    ppe = col(df, "固定资产净额", "固定资产及清理合计")
    ta = col(df, "资产总计")
    ni = col(df, "净利润")
    cfo = col(df, "经营活动产生的现金流量净额")
    cash = col(df, "货币资金")
    inventory = col(df, "存货")
    debt = col(df, "短期借款").fillna(0) + col(df, "长期借款").fillna(0) + col(df, "应付债券").fillna(0)
    fin_cost = col(df, "财务费用")
    # extra inputs for the 8-variable model
    dep = col(df, "固定资产折旧")
    sga = col(df, "销售费用").fillna(0) + col(df, "管理费用").fillna(0)
    cl = col(df, "流动负债合计")
    ltd = col(df, "长期借款").fillna(0) + col(df, "应付债券").fillna(0)

    gm = (sales - cogs) / sales
    aq = 1 - (ca + ppe) / ta
    dep_rate = dep / (dep + ppe)
    lev = (cl + ltd) / ta

    out = pd.DataFrame(index=df.index)
    out["营业收入(亿)"] = sales / 1e8
    out["净利润(亿)"] = ni / 1e8
    # Beneish components
    out["DSRI"] = (ar / sales) / (ar / sales).shift(1)
    out["GMI"] = gm.shift(1) / gm
    out["AQI"] = aq / aq.shift(1)
    out["SGI"] = sales / sales.shift(1)
    out["TATA"] = (ni - cfo) / ta
    out["DEPI"] = dep_rate.shift(1) / dep_rate
    out["SGAI"] = (sga / sales) / (sga / sales).shift(1)
    out["LVGI"] = lev / lev.shift(1)
    out["M_Score"] = (-6.065 + 0.823 * out["DSRI"] + 0.906 * out["GMI"]
                      + 0.593 * out["AQI"] + 0.717 * out["SGI"] + 7.770 * out["TATA"])
    out["M_Score_8"] = (-4.84 + 0.920 * out["DSRI"] + 0.528 * out["GMI"] + 0.404 * out["AQI"]
                        + 0.892 * out["SGI"] + 0.115 * out["DEPI"] - 0.172 * out["SGAI"]
                        + 4.679 * out["TATA"] - 0.327 * out["LVGI"])
    # China-specific red flags (unchanged from project 1)
    out["现金/总资产"] = cash / ta
    out["有息负债/总资产"] = debt / ta
    out["净现金(亿)"] = (cash - debt) / 1e8
    out["财务费用(亿)"] = fin_cost / 1e8
    out["财务费用/营业收入"] = fin_cost / sales
    out["经营现金流/净利润"] = cfo / ni
    out["3年经营现金流/净利润"] = cfo.rolling(3).sum() / ni.rolling(3).sum()
    out["存货增速-收入增速"] = inventory.pct_change(fill_method=None) - sales.pct_change(fill_method=None)
    return out.round(3)


def red_flags(row: pd.Series) -> list[str]:
    flags = []
    if row["M_Score"] > M5_THRESHOLD:
        flags.append(f"5变量M-Score {row['M_Score']:.2f} 高于阈值 {M5_THRESHOLD}")
    if pd.notna(row["M_Score_8"]) and row["M_Score_8"] > M8_THRESHOLD:
        flags.append(f"8变量M-Score {row['M_Score_8']:.2f} 高于阈值 {M8_THRESHOLD}")
    if row["现金/总资产"] > 0.2 and row["有息负债/总资产"] > 0.2:
        flags.append("存贷双高：现金和有息负债同时超过总资产的20%")
    if row["净现金(亿)"] > 0 and row["财务费用/营业收入"] > 0.01:
        flags.append("净现金为正但财务费用超过营收1%，现金真实性存疑")
    if row["3年经营现金流/净利润"] < 0.5:
        flags.append(f"近3年经营现金流仅覆盖净利润的 {row['3年经营现金流/净利润']:.0%}")
    if row["存货增速-收入增速"] > 0.2:
        flags.append("存货增速比收入增速高出20个百分点以上")
    return flags


def drivers(row: pd.Series, coef: dict, top: int = 2) -> str:
    """Biggest positive contributions vs a 'neutral' company (index = 1, TATA = 0).

    e.g. "AQI=3.79(+1.66); DSRI=1.26(+0.21)" -> AQI explains most of the score.
    """
    contrib = {k: c * (row[k] - (0 if k == "TATA" else 1)) for k, c in coef.items() if pd.notna(row[k])}
    best = sorted(((v, k) for k, v in contrib.items() if v > 0), reverse=True)[:top]
    return "; ".join(f"{k}={row[k]:.2f}(+{v:.2f})" for v, k in best)


def risk_level(n_flags: int) -> str:
    return "低" if n_flags == 0 else ("中" if n_flags == 1 else "高")


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.unicode.east_asian_width", True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    overview = []
    for code, name in COMPANIES.items():
        ind = compute_indicators(load_annual(code)).tail(N_YEARS)
        ind["红旗"] = ind.apply(lambda r: "; ".join(red_flags(r)), axis=1)
        ind["红旗数"] = ind["红旗"].apply(lambda s: len(s.split("; ")) if s else 0)
        ind["M5主要驱动"] = ind.apply(lambda r: drivers(r, M5_COEF), axis=1)
        ind["M8主要驱动"] = ind.apply(lambda r: drivers(r, M8_COEF), axis=1)
        ind.to_csv(OUT_DIR / f"{code}_fraud_risk.csv", encoding="utf-8-sig")
        latest = ind.iloc[-1]
        overview.append({"公司": name, "年度": int(ind.index[-1]), "M5": latest["M_Score"], "M8": latest["M_Score_8"],
                         "红旗数": int(latest["红旗数"]), "风险等级": risk_level(int(latest["红旗数"])),
                         "红旗": latest["红旗"]})
        if code == TARGET:
            target_ind = ind

    # Summary of the target company for the report writer
    t = target_ind
    summary = {
        "target": TARGET, "name": COMPANIES[TARGET], "years": [int(y) for y in t.index],
        "latest_year": int(t.index[-1]), "risk_level": risk_level(int(t["红旗数"].iloc[-1])),
        "risk_level_rule": "latest-year red flags: 0 = 低, 1 = 中, 2+ = 高",
        "thresholds": {"M5": M5_THRESHOLD, "M8": M8_THRESHOLD},
        "by_year": {int(y): {"M5": r["M_Score"], "M8": r["M_Score_8"],
                             "红旗": r["红旗"].split("; ") if r["红旗"] else [],
                             "M5主要驱动": r["M5主要驱动"], "M8主要驱动": r["M8主要驱动"],
                             "分项": {k: r[k] for k in VAR_MEANING}}
                    for y, r in t.iterrows()},
        "variable_meaning": VAR_MEANING,
        "driver_method": "contribution = coefficient x (index - 1), TATA vs 0; top positive contributions listed",
        "key_indicators_latest": {k: (None if pd.isna(t[k].iloc[-1]) else float(t[k].iloc[-1]))
                                  for k in ["现金/总资产", "有息负债/总资产", "净现金(亿)", "财务费用/营业收入",
                                            "经营现金流/净利润", "3年经营现金流/净利润", "存货增速-收入增速"]},
        "peers_latest": [o for o in overview if o["公司"] != COMPANIES[TARGET]],
    }
    (OUT_DIR / "fraud_risk.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{COMPANIES[TARGET]} ({TARGET}) — fraud-risk indicators")
    print(t[["M_Score", "M_Score_8", "现金/总资产", "有息负债/总资产", "财务费用/营业收入", "3年经营现金流/净利润",
             "存货增速-收入增速", "红旗数"]].to_string())
    for y, r in t.iterrows():
        if r["红旗"]:
            print(f"  {y}: {r['红旗']}")
            print(f"        M5 drivers: {r['M5主要驱动']}   M8 drivers: {r['M8主要驱动']}")
    print("\nLatest year, all companies")
    print(pd.DataFrame(overview).drop(columns=["红旗"]).to_string(index=False))
    for o in overview:
        if o["红旗数"]:
            print(f"  {o['公司']}: {o['红旗']}")
    print("\nSaved -> data/processed/{code}_fraud_risk.csv, fraud_risk.json")