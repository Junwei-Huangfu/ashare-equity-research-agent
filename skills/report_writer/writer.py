"""Skill 6a: Report writer — turn the structured outputs of Skills 2-4 into a Chinese equity research report.

Design principle: Python computes and FORMATS every number; the LLM only organises and explains them.
  1. build_facts()  collects the outputs of the other skills into one "facts pack" with pre-formatted
                    strings (e.g. "11.97%"), so the model copies numbers instead of calculating them.
  2. The rating is decided by a rule in config/report.toml, not by the model.
  3. The prompt forbids any number that is not in the facts pack (checked later by the evaluation skill).

Input : data/processed/*  (financial analysis, WACC, DCF, comps, valuation summary, fraud risk)
        reports/{code}_annual_report_qa.json  (annual-report RAG answers with page citations, optional)
        config/report.toml, .env (LLM_API_KEY, LLM_BASE_URL, LLM_MODEL)
Output: reports/{code}_facts.json        the facts pack (also used for number tracing)
        reports/{code}_prompt.md         the exact prompt sent to the model
        reports/{code}_draft.md          the model's draft report

Usage (run from the project root):
    python skills/report_writer/writer.py --dry-run    # build facts + prompt only, no API call, no cost
    python skills/report_writer/writer.py              # call the LLM and write the draft
"""
import json
import os
import sys
import time
import tomllib
from datetime import date
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROC = PROJECT_ROOT / "data" / "processed"
REPORTS = PROJECT_ROOT / "reports"
CONFIG = PROJECT_ROOT / "config" / "report.toml"

sys.path.insert(0, str(PROJECT_ROOT / "skills" / "data_fetch"))
from data_fetch import COMPANIES  # noqa: E402

TARGET = list(COMPANIES)[0]


# ---------------------------------------------------------------- formatting helpers
def pct(x, d=1):
    return "-" if x is None or pd.isna(x) else f"{x * 100:.{d}f}%"


def num(x, d=2):
    return "-" if x is None or pd.isna(x) else f"{x:,.{d}f}"


def fmt_metric(metric: str, v) -> str:
    """Same display rules as the financial analysis skill: amounts/days/multiples as numbers, ratios as %."""
    if pd.isna(v):
        return "-"
    plain = ("亿元" in metric or "天数" in metric
             or metric in ("杜邦_总资产周转率", "杜邦_权益乘数", "经营现金流/净利润", "收现比"))
    return num(v) if plain else pct(v)


def table_to_records(df: pd.DataFrame) -> dict:
    """{metric: {column: formatted value}}"""
    return {m: {str(c): fmt_metric(m, df.loc[m, c]) for c in df.columns} for m in df.index}


def peer_rankings(peers: pd.DataFrame, target_name: str) -> dict:
    """Rank the target among all companies for every metric, so the LLM never has to compare numbers itself.

    peers: rows = metrics, columns = company names (latest year).
    """
    out = {}
    n = peers.shape[1]
    for m in peers.index:
        row = peers.loc[m].dropna().sort_values(ascending=False)
        if target_name not in row.index or len(row) < 2:
            continue
        rank = list(row.index).index(target_name) + 1
        out[m] = {
            f"{target_name}排名(从高到低)": f"第{rank}/{len(row)}" if len(row) == n else f"第{rank}/{len(row)}(仅{len(row)}家有数据)",
            "最高": f"{row.index[0]} {fmt_metric(m, row.iloc[0])}",
            "最低": f"{row.index[-1]} {fmt_metric(m, row.iloc[-1])}",
            "从高到低": [f"{c} {fmt_metric(m, v)}" for c, v in row.items()],
        }
    return out


def load_json(name: str) -> dict:
    return json.loads((PROC / name).read_text(encoding="utf-8"))


def triggered(v: dict, th: dict) -> list[str]:
    """Which M-Score model(s) raised the alarm this year, with that model's own drivers."""
    out = []
    if v["M5"] is not None and v["M5"] > th["M5"]:
        out.append(f"5变量模型 (M5 {num(v['M5'])} > {th['M5']}): {v['M5主要驱动']}")
    if v["M8"] is not None and v["M8"] > th["M8"]:
        out.append(f"8变量模型 (M8 {num(v['M8'])} > {th['M8']}): {v['M8主要驱动']}")
    return out or ["无报警"]


# ---------------------------------------------------------------- rating rule
def rating(price: float, low: float, high: float, cfg: dict) -> tuple[str, float]:
    pos = (price - low) / (high - low)
    r = cfg["rating"]
    if pos < 0:
        label = "买入"
    elif pos < r["lower_third"]:
        label = "增持"
    elif pos <= r["upper_third"]:
        label = "中性"
    elif pos <= 1:
        label = "减持"
    else:
        label = "卖出"
    return label, pos


# ---------------------------------------------------------------- facts pack
def build_facts(cfg: dict) -> dict:
    name = COMPANIES[TARGET]
    fin = pd.read_csv(PROC / f"{TARGET}_financial_analysis.csv", index_col=0)
    peers = pd.read_csv(PROC / "peer_comparison.csv", index_col=0)
    wacc = load_json("wacc.json")
    dcf = load_json("dcf.json")
    summ = load_json("valuation_summary.json")
    risk = load_json("fraud_risk.json")
    fc = pd.read_csv(PROC / "dcf_forecast.csv", index_col=0)
    sens = pd.read_csv(PROC / "dcf_sensitivity.csv", index_col=0)
    comps = pd.read_csv(PROC / "comps.csv", index_col=0)

    t_row = comps.loc[name]
    a = dcf["assumptions"]
    low, high = summ["fair_value_range"]
    label, pos = rating(summ["price"], low, high, cfg)

    forecast = {}
    for y, r in fc.iterrows():
        forecast[y] = {"营业收入(亿元)": num(r["revenue"]), "营收增速": pct(r["growth"], 2),
                       "核心EBIT利润率": pct(r["ebit_margin"], 2), "税后经营利润(亿元)": num(r["nopat"]),
                       "折旧摊销(亿元)": num(r["da"]), "资本开支(亿元)": num(r["capex"]),
                       "营运资本增加(亿元)": num(r["delta_nwc"]), "自由现金流FCFF(亿元)": num(r["fcff"]),
                       "计入比例": num(r["fraction"]), "现值(亿元)": num(r["pv_fcff"])}

    facts = {
        "基本信息": {
            "公司": name, "代码": TARGET, "估值日": summ["valuation_date"], "报告日期": str(date.today()),
            "收盘价(元)": num(summ["price"]), "总股本(亿股)": num(dcf["shares_yi"]),
            "总市值(亿元)": num(wacc["market_cap"] / 1e8, 1),
            "可比公司": [c for c in COMPANIES.values() if c != name],
        },
        "评级与结论(由规则计算,不得更改)": {
            "评级": label,
            "评级规则": "现价在合理价值区间中的位置: <0 买入, 下1/3 增持, 中间 中性, 上1/3 减持, >1 卖出",
            "现价在区间中的位置": pct(pos, 0),
            "合理价值区间(元)": f"{num(low)} ~ {num(high)}",
            "区间依据": summ["fair_value_range_basis"],
            "DCF基准每股价值(元)": num(summ["dcf_base_value"]),
            "DCF基准相对现价空间": pct(summ["dcf_base_upside"]),
            "区间两端相对现价空间": f"{pct(summ['upside_at_range'][0])} ~ {pct(summ['upside_at_range'][1])}",
        },
        "财务分析(年度)": table_to_records(fin),
        "财务分析口径说明": {
            "有息负债": "年末 短期借款+长期借款+应付债券+一年内到期的非流动负债, 不含租赁负债",
            "净现金": "年末 货币资金 - 有息负债",
            "ROE(归母,平均)": "归母净利润 / 平均归母权益",
            "杜邦_ROE(全部权益)": "净利率 x 总资产周转率 x 权益乘数, 使用全部权益(含少数股东)",
        },
        "同业比较(最新年度)": table_to_records(peers),
        "同业排名(由Python计算,比较结论只能引用这里)": peer_rankings(peers, name),
        "WACC": {
            "无风险利率(10年国债)": pct(wacc["risk_free_rate"], 2), "无风险利率日期": wacc["risk_free_date"],
            "回归Beta": num(wacc["beta"]["raw_beta"]), "调整后Beta(Blume)": num(wacc["beta"]["adjusted_beta"]),
            "Beta回归R²": num(wacc["beta"]["r_squared"]), "回归周数": wacc["beta"]["n_weeks"],
            "Beta方法": "过去3年周度后复权收益率对沪深300回归, Blume调整 = 0.67 x 回归Beta + 0.33",
            "股权风险溢价": pct(wacc["equity_risk_premium"]), "股权成本": pct(wacc["cost_of_equity"], 2),
            "有息负债(亿元)": num(wacc["interest_bearing_debt"] / 1e8),
            "有息负债口径": f"{wacc['debt_report_date']} 最新已披露资产负债表, 含租赁负债和一年内到期的非流动负债"
                       "(与财务分析中的年末口径不同)",
            "股权权重": pct(wacc["weight_equity"], 2),
            "WACC": pct(wacc["wacc"], 2),
            "同业调整后Beta": {k: num(v["adjusted_beta"]) for k, v in wacc["peer_betas"].items()},
        },
        "DCF": {
            "方法": "FCFF = EBIT x (1-税率) + 折旧摊销 - 资本开支 - 营运资本增加; 以最新已披露资产负债表日为基准日",
            "基准日": dcf["base_date"],
            "假设": {
                "首年营收增速": pct(a["first_year_growth"], 2), "首年增速来源": "2026年上半年营收同比增速",
                "营收增速路径": [pct(x, 2) for x in a["growth_path"]],
                "核心EBIT利润率": f"从最新 {pct(a['ebit_margin_latest'], 2)} 线性回落至5年均值 {pct(a['ebit_margin_end'], 2)}",
                "有效税率(近3年平均)": pct(a["tax_rate"], 2), "折旧摊销/营收": pct(a["da_pct_revenue"], 2),
                "资本开支/营收": pct(a["capex_pct_revenue"], 2), "营运资本/营收": pct(a["nwc_pct_revenue"], 2),
                "永续增长率": pct(a["terminal_growth"], 2), "WACC": pct(a["wacc"], 2),
            },
            "预测表": forecast,
            "预测期现金流现值(亿元)": num(dcf["pv_explicit_fcff_yi"]),
            "终值现值(亿元)": num(dcf["pv_terminal_value_yi"]),
            "终值占企业价值比例": pct(dcf["terminal_value_share_of_ev"], 0),
            "企业价值(亿元)": num(dcf["enterprise_value_yi"]),
            "企业价值到股权价值调整(亿元)": {k: num(v) for k, v in dcf["bridge_yi"].items()},
            "股权价值(亿元)": num(dcf["equity_value_yi"]),
            "每股价值(元)": num(dcf["value_per_share"]),
            "DCF隐含PE(TTM)": num(summ["implied_pe_from_dcf"], 1) + "x",
            "敏感性分析(每股价值,元; 行=WACC, 列=永续增长率)": {
                w: {gcol: num(sens.loc[w, gcol]) for gcol in sens.columns} for w in sens.index},
        },
        "可比公司估值": {
            "统计方法": "同业中位数; 倍数<=0视为无意义并剔除",
            "口径说明(PE与EV/EBITDA为何结论不同)": {
                "非经营性净资产(亿元)": num(t_row["总市值(亿)"] - t_row["EV(亿)"]),
                "非经营性净资产占总市值": pct((t_row["总市值(亿)"] - t_row["EV(亿)"]) / t_row["总市值(亿)"]),
                "非经营性净资产含义": "货币资金 + 交易性金融资产等投资类资产 - 有息负债 - 少数股东权益(与DCF调整项相同)",
                "PE(TTM)": "分子是全部市值, 包含上述非经营性净资产; 账上现金和投资越多, PE 越显得低",
                "EV/EBITDA": "分子 EV = 市值 - 非经营性净资产, 只衡量核心经营业务; 5家公司用同一口径",
                "EV/EBITDA隐含每股价值的算法": "同业中位数 x 本公司EBITDA + 非经营性净资产(已加回), 再除以总股本",
                "本公司与同业中位数比较": {
                    "PE(TTM)": f"本公司 {num(t_row['PE(TTM)'])}x, 同业中位数 {num(summ['comps']['PE(TTM)']['peer_median'])}x, "
                               + ("本公司低于同业" if t_row["PE(TTM)"] < summ["comps"]["PE(TTM)"]["peer_median"] else "本公司高于同业"),
                    "EV/EBITDA": f"本公司 {num(t_row['EV/EBITDA'])}x, 同业中位数 {num(summ['comps']['EV/EBITDA']['peer_median'])}x, "
                                 + ("本公司低于同业" if t_row["EV/EBITDA"] < summ["comps"]["EV/EBITDA"]["peer_median"] else "本公司高于同业"),
                },
            },
            "倍数表": {c: {k: (num(v) if isinstance(v, float) else v) for k, v in r.items() if k != "code"}
                    for c, r in comps.iterrows()},
            "隐含每股价值": {k: {"本公司倍数": num(v["target_multiple"]) + "x",
                           "同业中位数": num(v["peer_median"]) + "x",
                           "隐含每股价值(元)": num(v["implied_price"]),
                           "同业25%~75%分位对应价值(元)": f"{num(v['implied_price_p25'])} ~ {num(v['implied_price_p75'])}",
                           "是否落在DCF合理区间内": "是" if summ["comps_within_dcf_range"][k] else "否"}
                       for k, v in summ["comps"].items()},
        },
        "财务风险筛查": {
            "方法": "Beneish M-Score 5变量(阈值-2.22) 与 8变量(阈值-1.78), 加A股特色红旗规则",
            "最新年度风险等级": risk["risk_level"], "风险等级规则": "最新年度红旗数: 0=低, 1=中, 2个及以上=高",
            "逐年": {y: {"M5": num(v["M5"]), "M8": num(v["M8"]), "红旗": v["红旗"] or ["无"],
                       "M5主要驱动": v["M5主要驱动"] or "-", "M8主要驱动": v["M8主要驱动"] or "-",
                       "触发报警的模型及其驱动": triggered(v, risk["thresholds"])}
                   for y, v in risk["by_year"].items()},
            "主要驱动计算方法": "贡献 = 系数 x (指数 - 1), TATA 与 0 比较; 列出贡献最大的正向变量, 括号内为对分数的贡献",
            "变量含义": risk["variable_meaning"],
            "同业最新年度": [{"公司": p["公司"], "红旗数": p["红旗数"], "风险等级": p["风险等级"]}
                         for p in risk["peers_latest"]],
        },
    }
    qa = annual_report_evidence()
    if qa:
        facts["年报证据(RAG检索年报原文, 含页码)"] = qa
    return facts


def annual_report_evidence() -> list[dict]:
    """Answers from the annual-report RAG skill (only citations that passed the page check are kept)."""
    path = REPORTS / f"{TARGET}_annual_report_qa.json"
    if not path.exists():
        return []
    out = []
    for item in json.loads(path.read_text(encoding="utf-8")):
        a = item.get("llm")
        if not a:
            continue
        out.append({"问题": item["question"], "年报回答": a["answer"],
                    "证据是否充分": "是" if a.get("sufficient") else "否(部分信息年报片段未覆盖)",
                    "已核验的页码引用": a["valid_citations"]})
    return out


# ---------------------------------------------------------------- prompt
SYSTEM_PROMPT = """你是一名严谨的A股卖方医药行业分析师，负责撰写公司深度研究报告。
你只能使用用户提供的"事实数据包"中的数据。必须遵守以下规则：
1. 报告中出现的每一个数字，都必须原样来自事实数据包（保留相同的写法和小数位），禁止自行计算、换算、四舍五入或编造任何新数字。
2. 需要比较时，用文字描述方向和程度（如"明显高于""小幅回落"），不要计算差值或比例。
3. 评级和合理价值区间已由规则确定，必须原样使用，不得修改或给出其他目标价。
4. 事实数据包没有提供的信息（如具体产品、管理层、行业政策、某个指标变化的业务原因），可以提出合理推测，但必须明确标注"（待年报验证）"，不得当作事实陈述。
5. 对模型结果要有专业判断：例如 M-Score 报警时，结合"主要驱动"变量解释可能原因，并说明是否可能是误报。
6. 凡是"最高""最低""第几""高于/低于同业""持平"等比较结论，只能引用"同业排名"或"本公司与同业中位数比较"中已给出的结果，不得自己比较数字。
7. 解释 M-Score 报警时，只引用"触发报警的模型及其驱动"中对应模型的驱动变量。
8. 解释 PE 与 EV/EBITDA 结论差异时，以"口径说明"为准。
9. 同一名称的指标若有不同口径（如有息负债），引用时注明口径。
10. "年报证据"是从年报原文检索得到的回答。凡是年报证据已经回答的问题（如费用增加原因、投资对象、业务结构、风险），直接引用其结论，并保留页码出处，格式如（2025年报第198页），不要再标注"待年报验证"；年报证据中的数字可以原样引用。年报证据标明"证据不足"的部分，仍需标注"（待年报验证）"。
11. 当年报证据与模型推测不一致时，以年报证据为准，并指出推测被修正。
12. 语言专业、客观、简洁，使用中文。输出 Markdown 格式。"""

REPORT_OUTLINE = """请撰写 {name}（{code}）公司深度研究报告，结构如下：

# {name}（{code}）深度研究报告：标题（一句话概括核心观点）

**评级：XX ｜ 合理价值区间：XX ~ XX 元 ｜ 现价：XX 元（估值日 XX）**

## 一、投资要点
3-5 条要点，每条一句结论 + 关键数据支撑。

## 二、财务表现分析
盈利能力、成长性、杜邦分析（ROE 由什么驱动）。

## 三、现金流与资产负债表质量
经营现金流质量、资本开支、营运效率、现金与投资资产。

## 四、同业比较
与可比公司在盈利、效率、估值上的对比，以及为什么选这些可比公司。

## 五、估值分析
5.1 WACC 推导；5.2 DCF 关键假设与结果（含预测表、企业价值到股权价值的调整）；
5.3 敏感性分析（说明现价隐含的折现率大约在什么水平）；5.4 可比公司估值与交叉验证（解释 PE 与 EV/EBITDA 结论不同的原因）；
5.5 估值结论。

## 六、财务风险筛查
M-Score 与红旗规则结果，解释报警年份的主要驱动因素及判断。

## 七、风险提示
至少 4 条，结合数据。

---
免责声明：本报告由 AI 投研系统基于公开数据自动生成，仅用于技术展示，不构成任何投资建议。

以下是事实数据包（JSON）：
````json
{facts}
```"""


def build_prompt(facts: dict) -> str:
    return REPORT_OUTLINE.format(name=COMPANIES[TARGET], code=TARGET,
                                 facts=json.dumps(facts, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- LLM call
def call_llm(system: str, user: str, cfg: dict) -> tuple[str, dict]:
    from openai import OpenAI  # imported here so --dry-run works without the package

    client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
    model = os.environ["LLM_MODEL"]
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=cfg["llm"]["temperature"], max_tokens=cfg["llm"]["max_tokens"],
        # DeepSeek V4 thinks by default, and thinking tokens count towards max_tokens.
        # Here all numbers and reasoning are already done by Python, so thinking is switched off in config.
        extra_body={"thinking": {"type": cfg["llm"]["thinking"]}},
    )
    usage = {"model": model, "seconds": round(time.time() - t0, 1),
             "prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens,
             "finish_reason": getattr(resp.choices[0], "finish_reason", None)}
    if usage["finish_reason"] == "length":
        print("WARNING: the model hit max_tokens and the report is cut off -> raise max_tokens in config/report.toml")
    text = resp.choices[0].message.content or ""
    if not text.strip():
        raise RuntimeError("The model returned an empty report (all tokens may have gone to thinking). "
                           "Check `thinking` and `max_tokens` in config/report.toml.")
    return text, usage


if __name__ == "__main__":
    load_dotenv(PROJECT_ROOT / ".env")
    cfg = tomllib.load(open(CONFIG, "rb"))
    REPORTS.mkdir(parents=True, exist_ok=True)

    facts = build_facts(cfg)
    prompt = build_prompt(facts)
    (REPORTS / f"{TARGET}_facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS / f"{TARGET}_prompt.md").write_text(SYSTEM_PROMPT + "\n\n" + prompt, encoding="utf-8")
    r = facts["评级与结论(由规则计算,不得更改)"]
    print(f"Facts pack built: rating {r['评级']}, fair value {r['合理价值区间(元)']} 元, "
          f"price at {r['现价在区间中的位置']} of the range")
    print(f"Prompt length: {len(SYSTEM_PROMPT) + len(prompt):,} characters")
    print(f"Saved -> reports/{TARGET}_facts.json, reports/{TARGET}_prompt.md")

    if "--dry-run" in sys.argv:
        print("Dry run: no API call made.")
        sys.exit(0)

    print(f"Calling {os.environ.get('LLM_MODEL', 'LLM')} ... (this can take 1-3 minutes)")
    text, usage = call_llm(SYSTEM_PROMPT, prompt, cfg)
    (REPORTS / f"{TARGET}_draft.md").write_text(text, encoding="utf-8")
    (REPORTS / f"{TARGET}_draft_usage.json").write_text(json.dumps(usage, indent=2), encoding="utf-8")
    print(f"Done in {usage['seconds']}s  tokens in/out: {usage['prompt_tokens']:,} / {usage['completion_tokens']:,}")
    print(f"Saved -> reports/{TARGET}_draft.md")