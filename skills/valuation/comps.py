"""Skill 3c: Valuation — comparable companies (PE, PB, EV/EBITDA) + final valuation summary.

Input : config/valuation.toml, data/processed/dcf.json + dcf_sensitivity.csv (run dcf.py first)
        data/raw/{code}_估值行情.csv / 利润表.csv / 资产负债表.csv / 折旧摊销.csv  for all companies
Output: data/processed/comps.csv               (multiples of every company)
        data/processed/valuation_summary.json  (single file the report writer reads)

PE (TTM) and PB come straight from East Money for the valuation date.
EV/EBITDA is built from the statements:
    EBITDA (TTM) = core EBIT (TTM) + D&A (TTM)       TTM = last annual + this H1 - last H1
    EV           = market cap + debt + minority - cash - non-operating assets   (same items as the DCF bridge)
Implied value for the target = peer median multiple x target's own metric (+ bridge items for EV/EBITDA).

Usage (run from the project root):
    python skills/valuation/wacc.py
    python skills/valuation/dcf.py
    python skills/valuation/comps.py
"""
import json
import sys
import tomllib
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG = PROJECT_ROOT / "config" / "valuation.toml"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "valuation"))
from data_fetch import COMPANIES  # noqa: E402
from dcf import g, latest_published_bs, market_row, read  # noqa: E402  (reuse DCF helpers)

YI = 1e8


def ttm(df: pd.DataFrame, col_values: pd.Series, h1_date: str) -> float:
    """Trailing twelve months = last annual + this H1 - last H1."""
    year = int(h1_date[:4])
    v = col_values.set_axis(df["报告日"])
    return float(v[f"{year - 1}1231"] + v[h1_date] - v[f"{year - 1}0630"])


def company_multiples(code: str, cfg: dict, end: pd.Timestamp) -> dict:
    br = cfg["bridge"]
    mk = market_row(code, end)
    bs = latest_published_bs(code, end)
    h1 = bs["报告日"]                                   # e.g. 20260630 (latest published period)

    inc = read(code, "利润表")
    core_ebit = (inc["营业收入"] - inc["营业成本"] - g(inc, "营业税金及附加")
                 - g(inc, "销售费用") - g(inc, "管理费用") - g(inc, "研发费用"))
    dna = read(code, "折旧摊销")
    ebitda = ttm(inc, core_ebit, h1) + ttm(dna, dna["折旧摊销合计"], h1)

    num = lambda k: float(bs[k]) if k in bs.index and pd.notna(bs[k]) else 0.0  # noqa: E731
    cash_and_non_op = num("货币资金") + sum(num(k) for k in br["add_non_operating"])
    debt = sum(num(k) for k in br["subtract_debt"])
    minority = num(br["subtract_minority"])
    mcap = float(mk["总市值"])
    ev = mcap + debt + minority - cash_and_non_op

    return {"code": code, "公司": COMPANIES[code], "收盘价": float(mk["当日收盘价"]),
            "总市值(亿)": round(mcap / YI, 2), "PE(TTM)": round(float(mk["PE(TTM)"]), 2),
            "PB": round(float(mk["市净率"]), 2), "EV(亿)": round(ev / YI, 2),
            "EBITDA_TTM(亿)": round(ebitda / YI, 2), "EV/EBITDA": round(ev / ebitda, 2),
            "_bridge_net": cash_and_non_op - debt - minority, "_ebitda": ebitda, "_shares": float(mk["总股本"]),
            "_bs_date": h1}


if __name__ == "__main__":
    cfg = tomllib.load(open(CONFIG, "rb"))
    target = cfg["general"]["target"]
    end = pd.Timestamp(cfg["general"]["valuation_date"])

    rows = {c: company_multiples(c, cfg, end) for c in COMPANIES}
    t = rows[target]
    peers = pd.DataFrame([r for c, r in rows.items() if c != target])

    # ---- implied value per share for the target from each peer multiple
    # A multiple <= 0 is meaningless (loss-making, or EV < 0 because cash exceeds market value): excluded
    stat = cfg["comps"]["statistic"]
    mult = peers.set_index("公司")[["PE(TTM)", "PB", "EV/EBITDA"]]
    valid = mult.where(mult > 0)
    excluded = {k: list(valid.index[valid[k].isna()]) for k in valid.columns}
    agg, q25, q75 = valid.agg(stat), valid.quantile(0.25), valid.quantile(0.75)

    def implied(multiple: str, m: float) -> float:
        if multiple == "EV/EBITDA":
            return (m * t["_ebitda"] + t["_bridge_net"]) / t["_shares"]
        return t["收盘价"] * m / t[multiple]        # price x (peer multiple / own multiple)

    comps_result = {}
    for k in ["PE(TTM)", "PB", "EV/EBITDA"]:
        comps_result[k] = {"target_multiple": t[k], "peer_" + stat: round(float(agg[k]), 2),
                           "peer_p25": round(float(q25[k]), 2), "peer_p75": round(float(q75[k]), 2),
                           "implied_price": round(implied(k, agg[k]), 2),
                           "implied_price_p25": round(implied(k, q25[k]), 2),
                           "implied_price_p75": round(implied(k, q75[k]), 2),
                           "peers_used": int(valid[k].notna().sum()), "peers_excluded": excluded[k]}

    # ---- final summary: DCF point + range, comps as cross-check
    dcf = json.loads((OUT_DIR / "dcf.json").read_text(encoding="utf-8"))
    sens = pd.read_csv(OUT_DIR / "dcf_sensitivity.csv", index_col=0)
    g_col = f"{cfg['dcf']['terminal_growth']:.2%}"
    lo_row, hi_row = f"{cfg['conclusion']['wacc_high']:.1%}", f"{cfg['conclusion']['wacc_low']:.1%}"
    range_low, range_high = float(sens.loc[lo_row, g_col]), float(sens.loc[hi_row, g_col])
    price = t["收盘价"]
    in_range = {k: bool(range_low <= v["implied_price"] <= range_high) for k, v in comps_result.items()}

    summary = {
        "target": target, "name": COMPANIES[target], "valuation_date": str(end.date()), "price": price,
        "dcf_base_value": dcf["value_per_share"], "dcf_base_upside": dcf["upside"],
        "fair_value_range": [range_low, range_high],
        "fair_value_range_basis": f"DCF, terminal growth {g_col}, WACC {lo_row} to {hi_row}",
        "upside_at_range": [round(range_low / price - 1, 4), round(range_high / price - 1, 4)],
        "comps": comps_result, "comps_within_dcf_range": in_range,
        "implied_pe_from_dcf": round(dcf["equity_value_yi"] * YI / (t["总市值(亿)"] * YI / t["PE(TTM)"]), 2),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table = pd.DataFrame(rows.values()).drop(columns=[c for c in t if c.startswith("_")]).set_index("公司")
    table.to_csv(OUT_DIR / "comps.csv", encoding="utf-8-sig")
    (OUT_DIR / "valuation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- print
    print(f"Comparable companies (valuation date {end.date()}, balance sheet {t['_bs_date']})")
    print(table.drop(columns=["code"]).to_string())
    print(f"\nImplied value per share for {COMPANIES[target]} (peer {stat}; p25 ~ p75 in brackets)")
    for k, v in comps_result.items():
        print(f"  {k:<10} own {v['target_multiple']:>6.2f}x  peer {v['peer_' + stat]:>6.2f}x"
              f"  -> {v['implied_price']:>6.2f} 元  [{v['implied_price_p25']:.2f} ~ {v['implied_price_p75']:.2f}]"
              + (f"   excluded (<=0): {', '.join(v['peers_excluded'])}" if v["peers_excluded"] else ""))
    print(f"\nValuation summary  (price {price:.2f})")
    print(f"  DCF base case        {summary['dcf_base_value']:.2f} 元  ({summary['dcf_base_upside']:+.1%})")
    print(f"  Fair value range     {range_low:.2f} ~ {range_high:.2f} 元  ({summary['fair_value_range_basis']})")
    print(f"  DCF implied PE(TTM)  {summary['implied_pe_from_dcf']:.1f}x")
    for k, ok in in_range.items():
        print(f"  {k:<10} median implied price {'inside' if ok else 'OUTSIDE'} the DCF range")
    print("\nSaved -> data/processed/comps.csv, valuation_summary.json")