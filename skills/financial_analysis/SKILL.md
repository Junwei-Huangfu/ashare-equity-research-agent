---
name: financial_analysis
description: 由三张报表计算盈利能力、成长性、杜邦分析、现金流质量、偿债与营运效率等约27个指标，并生成可比公司最新年度对比表。需要公司财务表现或同业对比时调用。
---

# 技能 2：财务分析

## 输入
`data/raw/{code}_资产负债表/利润表/现金流量表.csv`（技能 1）

## 输出（`data/processed/`）
- `{code}_financial_analysis.csv`：行 = 指标，列 = 最近 5 个财年
- `peer_comparison.csv`：最新年度，全部公司并列

## 运行
```
python skills/financial_analysis/financial_analysis.py
```

## 关键口径
- 只用年报（报告日 1231），各年口径一致。
- ROE、ROA、周转率用**期初期末平均**余额，因此多读取一年数据。
- 杜邦分析用全部权益（含少数股东），使三因子相乘严格等于 ROE。
- 有息负债 = 短期借款 + 长期借款 + 应付债券 + 一年内到期的非流动负债。
- 新浪 2018–2019 年把应收账款并入"应收票据及应收账款"，代码自动兜底。

## 原则
所有数字由 Python 计算；大模型不做任何算术。
