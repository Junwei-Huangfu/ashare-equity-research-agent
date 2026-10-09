---
name: valuation
description: 估值技能。wacc.py 用CAPM和Beta回归计算WACC；dcf.py 做FCFF折现、企业价值到股权价值调整和敏感性分析；comps.py 做PE/PB/EV-EBITDA可比公司估值并输出估值总结。所有假设集中在 config/valuation.toml。
---

# 技能 3：估值

## 输入
- `config/valuation.toml`：**全部人工假设**（ERP、预测期、永续增长率、利润率路径、调整项、敏感性区间）
- `data/raw/` 中的行情、报表、折旧摊销、国债收益率

## 输出（`data/processed/`）
`wacc.json`、`dcf.json`、`dcf_forecast.csv`、`dcf_sensitivity.csv`、`comps.csv`、`valuation_summary.json`

## 运行（顺序固定）
```
python skills/valuation/wacc.py
python skills/valuation/dcf.py
python skills/valuation/comps.py
```

## 关键设计与判断
| 环节 | 做法 | 理由 |
|---|---|---|
| Beta | 3年周度后复权收益率对沪深300回归 + Blume调整 | 日度噪音大、月度样本少；后复权消除除息影响 |
| 无风险利率 | 估值日的10年期国债收益率 | 可溯源，不手填 |
| 收入增速 | 首年锚定2026H1同比，线性降至永续增长率 | 用真实数据起步，避免拍脑袋 |
| 利润率 | 由最新值线性回归到5年均值 | 利润率波动中回落的判断 |
| 基准日 | 最新**已公布**资产负债表日 | 避免未来信息（look-ahead bias） |
| EV→股权 | 加回超额现金、交易性金融资产、长期股权投资等；扣除有息负债、租赁负债、少数股东权益 | 长期股权投资收益不在主营EBIT中，不加回会低估 |
| 可比公司 | 取中位数；倍数≤0自动剔除；EV口径与DCF调整项一致 | 片仔癀高估值会拉高均值 |
| 结论 | DCF为点估计，WACC 6%–8% 给出合理区间，可比公司只做交叉验证 | 不让模型迎合股价，用区间表达分歧 |

## 已知局限
长期股权投资按账面值计入（市值法更准确）；终值占企业价值约84%，结论高度依赖WACC与永续增长率。
