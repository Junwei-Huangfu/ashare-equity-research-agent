我们需要审稿。用户要求只输出JSON。需要逐段通读初稿，对照事实数据包，找问题。必须真实，引用原文不超过40字，说明数据包依据，severity，type，location，quote，problem，evidence，fix。需要仔细。

我们需要检查所有数字、一致性、引用、口径、比较结论。 自动评测 already says numbers traced all, rating ok, range ok, missing none, open items 4. Need find real issues not just traceability. We need inspect draft.

Let's parse facts.

Data pack:
基本信息: 收盘价50.89, 总市值908.0, 总股本17.84.
评级与结论: 增持; 位置2%; 合理价值区间50.51~68.09; DCF基准68.34; 空间34.3%; 区间两端 -0.8% ~ 33.8%.
Finance etc.

Need compare draft.

Let's go section by section.

Title: "现金充裕、盈利改善的低估值中药龙头，DCF基准价值较现价存在三成以上空间" - ok? 34.3% yes.

Rating header: "增持 ｜ 合理价值区间：50.51 ~ 68.09 元 ｜ 现价：50.89 元（估值日 2026-10-08）" ok. "现价在合理价值区间中的位置为 2%，按既定规则对应"增持"评级。DCF 基准每股价值 68.34 元，相对现价空间 34.3%；区间两端相对现价空间为 -0.8% ~ 33.8%。" ok.

一、投资要点

1. "2025 年归母净利润 51.53 亿元，在可比公司中排名第 1/5；净利率由 2021 年 7.7% 逐年提升至 2025 年 12.6%，同期总资产周转率由 0.68 升至 0.77，权益乘数稳定在 1.36，ROE（归母，平均）由 7.3% 升至 13.1%。" 
Check: "权益乘数稳定在 1.36" - 2021 1.40, 2022 1.37, 2023 1.37, 2024 1.35, 2025 1.36. "稳定在1.36" slightly inaccurate but acceptable? Not necessarily. But issue? 低 maybe. Also ROE归母 from 7.3 to 13.1 yes.
"净利率由2021年7.7%逐年提升" actually 2021 7.7, 2022 7.8, 2023 10.5, 2024 11.9, 2025 12.6 yes. 总资产周转率 from 0.68 to 0.77 yes.
Potential type B? Not significant.

2. "2025 年营收增速 2.9%、归母净利润增速 8.5%，归母净利润增速在可比公司中排名第 1/5，而片仔癀、同仁堂同期归母净利润增速为负。" Check data: 华润三九 1.6, 白云山 5.2, 片仔癀 -27.5, 同仁堂 -22.1. yes.

3. "2025 年资产负债率 26.0%，有息负债（年末短期借款+长期借款+应付债券+一年内到期的非流动负债，不含租赁负债）仅 3.46 亿元，在可比公司中排名第 5/5（即最低）；净现金（年末货币资金-有息负债）87.62 亿元，排名第 1/5。" yes. 有息负债排名第5/5 from 从高到低 means lowest. yes.

4. "2025 年收现比 1.10，在可比公司中排名第 1/5；但经营现金流/净利润为 0.89，排名第 3/5，且应收账款周转天数 88.99 天，在可比公司中排名第 1/5（即最长）。" yes.

5. "PE(TTM) 17.39x 低于同业中位数 23.16x，而 EV/EBITDA 11.54x 高于同业中位数 10.84x，差异主要源于公司非经营性净资产占总市值 30.8%（口径说明）。" yes.

二、财务表现

2.1 "公司毛利率由 2021 年 27.2% 提升至 2025 年 29.5%，净利率同期由 7.7% 提升至 12.6%，提升幅度明显大于毛利率。费用端看，管理费用率由 3.0% 降至 2.5%，财务费用率由 -0.7% 收敛至 -0.1%，研发费用率稳定在 0.9% 附近，而销售费用率由 10.7% 上升至 13.6%，是费用端唯一明显上行的项目。" ok.

"关于销售费用率上升，年报证据显示... 2025 年销售费用合计 56.19 亿元，较上期 48.80 亿元增加... 公司说明主要是线上销售费用增加，带动线上营（原文截断）." The draft says "公司说明主要是线上销售费用增加（2025年报第198页）" It omits truncated "带动线上营" but fine.

"2024 年报显示销售费用同比下降 2.26%，公司解释为持续推进降本增效（2024年报第224页、第25页）；2023 年报显示销售费用同比增长 19.84%，原因为本期销售规模增长（2023年报第26页）。需注意，年报片段未提供 2021 年及 2025 年销售费用率的计算依据和具体解释，因此销售费用率长期上行的完整归因仍需结合后续披露观察（待年报验证）。"
Check facts: 年报回答 says "年报片段未提供2021年销售费用率10.7%的数据，也未提供2025年销售费用率13.6%的数据，因此无法直接解释该比率上升的原因." Draft says "年报片段未提供 2021 年及 2025 年销售费用率的计算依据和具体解释" ok. But it also states 2025 sales expense increased and components from annual report p198. That is evidence enough, but then marks 待年报验证 for long-term attribution. Is this violating F? "年报证据已回答却仍标待年报验证；年报证据不足却当作事实陈述." Need examine. For 销售费用率: evidence partially not provided for rates, but draft uses numeric ratios and expense details. It marks "销售费用率长期上行的完整归因仍需结合后续披露观察（待年报验证）" This is not exactly "answered yet marked待验证"? Data says evidence not sufficient: "否(部分信息年报片段未覆盖)". So marking待验证 acceptable? But open_items count 4, automatic says 4. Here three? Need see all. Not issue maybe.

"毛利率提升的业务结构原因方面... 2025 年工业销售收入 160.16 亿元，占营业收入 38.89%，毛利率 65.19%；商业销售收入 250.83 亿元，占 60.90%（2025年报第22页、第23页）。2024 年工业销售收入 144.68 亿元，占 36.14%，毛利率 65.93%，较上年同期增长 1.69 个百分点（2024年报第22页、第15页）。2024 年报提及业务结构持续优化、工业收入占比提升至 36.14%、提质增效举措成效显著，但未具体说明毛利率提升的直接原因（2024年报第15页、第45页）。据此推测，工业收入占比提升对整体毛利率有正向拉动（待年报验证）。"
Potential issue: "据此推测，工业收入占比提升对整体毛利率有正向拉动" - Is this inference from data? Data: 工业毛利率65.19%, 商业毛利率未提供. 占比提升 from 2024 36.14% to 2025 38.89%, overall gross margin 27.9% to 29.5%. Since industrial margin much higher than overall, if commercial omitted, plausible. Marked待验证. But maybe "待年报验证" on an inference is appropriate. Not issue? Could be "年报证据不足却当作事实陈述"? They phrase "据此推测" and "待年报验证" so ok.

Potential issue: "毛利率提升幅度明显大于毛利率" awkward maybe. Actually "净利率同期由7.7%提升至12.6%，提升幅度明显大于毛利率" okay.

2.2 "营收增速 2021-2025 年分别为 11.1%、0.3%、7.2%、2.4%、2.9%，整体处于低速增长区间；归母净利润增速分别为 -49.1%、7.0%、36.4%、16.0%、8.5%，2021 年为低基数年份，此后逐年回落但仍保持正增长。2025 年归母净利润增速 8.5%，在可比公司中排名第 1/5，明显好于同业中位数水平所反映的行业景气度。"

Check "2021年为低基数年份" - Is that accurate? 2021 net profit growth -49.1%, not low base? Wait if 2021 net profit dropped 49.1%, that creates low base for 2022? The phrasing "2021 年为低基数年份" may be backwards: 2021 was a high base? Need evaluate. Data: 2021 归母净利润 28.05, growth -49.1%. That means 2021 profit sharply declined; therefore 2021 is a low base year, leading to 2023 growth 36.4? Hmm "2021 年为低基数年份，此后逐年回落但仍保持正增长" Actually sequence: 2021 growth -49.1% (低基数? 2021 profit low relative to 2020), then 2022 +7.0, 2023 +36.4, 2024 +16.0, 2025 +8.5. So 2021 net profit was low, providing low base for subsequent high growth in 2023? But "此后逐年回落" maybe after 2023. Not a serious issue.

"明显好于同业中位数水平所反映的行业景气度" Hmm data does not have "同业中位数水平" for net profit growth? It has 同业排名 only and values. We can compute median of growth values? Comparable net profit growth: 云南8.5, 片仔癀-27.5, 同仁堂-22.1, 白云山5.2, 华润三九1.6. Sorted: -27.5, -22.1, 1.6, 5.2, 8.5 -> median 1.6. "同业中位数水平所反映的行业景气度" = 1.6, 云南8.5明显好于. This is an inference but not explicitly in data? Auto trace? It says "明显好于同业中位数水平" but data包 has no "同业中位数" except PE etc. Could be acceptable as narrative. However "明显好于同业中位数水平所反映的行业景气度" maybe a bit vague. Not a clear factual error.

2.3 "按全部权益口径（净利率 × 总资产周转率 × 权益乘数），ROE 由 2021 年 7.3% 提升至 2025 年 13.1%。拆解看：净利率：7.7% → 12.6%，是 ROE 提升的最主要来源；总资产周转率：0.68 → 0.77，贡献次之；权益乘数：1.40 → 1.36，小幅下行，说明 ROE 提升并非依赖加杠杆。即公司 ROE 改善是"利润率扩张 + 资产周转加快"的良性组合，而非财务杠杆驱动。2025 年杜邦 ROE（全部权益）13.1%，在可比公司中排名第 2/5。"

Check data: 杜邦_ROE全部权益 from 2021 7.3 to 2025 13.1. yes. 净利率 7.7→12.6; 总资产周转率0.68→0.77; 权益乘数1.40→1.36. yes. ranking 第2/5. yes. Good.

三、现金流与资产负债表质量

3.1 "2025 年经营现金流 46.00 亿元，在可比公司中排名第 2/5。收现比 1.10，在可比公司中排名第 1/5... 经营现金流/净利润为 0.89，排名第 3/5，且该比值自 2021 年 1.87 逐年回落至 2025 年 0.89，说明利润的现金含量较早年有所下降."

Check "该比值自2021年1.87逐年回落" Data: 2021 1.87, 2022 1.13, 2023 0.85, 2024 0.90, 2025 0.89. Not逐年回落; 2024 increased from 0.85 to 0.90, 2025 decreased to 0.89. Draft says "自 2021 年 1.87 逐年回落至 2025 年 0.89" – this is inaccurate because 2022 1.13 -> 2023 0.85 -> 2024 0.90 (上升) -> 2025 0.89. This is a数字/前后矛盾? It's a描述错误. Should say整体回落或自2021年高点回落, 但非逐年. Severity 中/低? It affects professional/accuracy but maybe not investment judgment. Type A? It's a calculated trend not matching data. Need issue. Quote within 40 chars: "且该比值自 2021 年 1.87 逐年回落至 2025 年 0.89" (24? ok) or "该比值自 2021 年 1.87 逐年回落至 2025 年 0.89" length around 25. Evidence: 2023 0.85, 2024 0.90, 2025 0.89，并非逐年. Fix: "由2021年1.87整体回落至0.89，其中2024年小幅回升至0.90". Severity 中.

Then "这一变化与营运资本占用上升方向一致：应收账款周转天数由 2021 年 53.88 天上升至 2025 年 88.99 天..." ok.

年报 evidence about AR. "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元，占比 93.49%，其中客户A占 42.23%、客户B占 30.78%（2025年报第237页）；但 2025 年报第164页另示前五名合计 18.87 亿元、占比 16.98%，两处口径存在差异。账龄信息仅 2021 年报第274页提及 3 年以上 318,264,739.09 元，2025 年账龄未提供。因此应收账款周转天数拉长的完整原因及账龄结构仍需后续披露验证（待年报验证）。"

Check data: 2025年报第164页前五名合计18.87亿元、占比16.98%? Data says "但2025年报第164页另示前五名合计18.87亿元、占比16.98%". ok. But note: "前五名客户合计应收账款和合同资产 18.52 亿元，占比 93.49%" in data yes. draft ok. 是.

3.2 "资本开支 2025 年 4.80 亿元，资本开支/营收 1.2%，在可比公司中排名第 5/5（即最低），属于典型的轻资本开支模式。自由现金流 2025 年 41.20 亿元，在可比公司中排名第 2/5，且自 2022 年 27.63 亿元的低点持续回升。"
Check 自由现金流: 2021 46.89, 2022 27.63, 2023 29.27, 2024 36.22, 2025 41.20 yes持续回升. ok.

3.3 "资产负债率 2021-2025 年稳定在 25.8%~27.8% 区间，2025 年为 26.0%，在可比公司中排名第 4/5（即偏低）。" Data: 2021 26.6, 2022 27.8, 2023 25.8, 2024 26.6, 2025 26.0; range 25.8-27.8 yes. 排名第4/5 from high = lower? There are 5: 白云山52.6, 华润三九34.6, 同仁堂30.2, 云南白药26.0, 片仔癀14.1. Ranking from high: 4th means 2nd lowest, so "偏低" ok. "在可比公司中排名第4/5（即偏低）" yes.

"有息负债（年末口径）由 2021 年 19.12 亿元大幅降至 2025 年 3.46 亿元，在可比公司中排名第 5/5（即最低）。净现金（年末货币资金-有息负债）2025 年 87.62 亿元，在可比公司中排名第 1/5。"

Investment assets para: "交易性金融资产期末余额为 4,192,113,408.43 元（2025年报第160页）" Data says same. ok.
"委托理财中银行理财产品余额 192,000 万元、券商理财产品余额 225,000 万元（2025年报第88页）" ok.

"此外，年报证据显示 2021-2022 年长期股权投资大幅增加，主要投资对象为上海医药集团股份有限公司：2021 年公司拟作为战略投资者以现金认购上海医药非公开发行的 665,626,796 股 A 股股票，认购金额不超过人民币 11,229,124,048.52 元，预计占上海医药发行后总股本的 18.02%（2021年报第104页）；2022 年该投资采用权益法核算，持股比例为 18.00%（2022年报第246页）；截至 2022 年末该长期股权投资账面价值为 11,318,607,693.92 元（2022年报第203页）。"

Ok.

四、同业比较

可比公司选择理由 ok? It says "均具备'老字号 + 品牌溢价'的估值特征" But 白云山? Is it? Might be not issue.

4.1 table and interpretation. Need verify all table numbers.
营业收入 411.87 rank2 yes.
归母净利润 rank1 yes.
毛利率29.5 rank4 yes.
净利率12.6 rank3 yes.
ROE归母13.1 rank3 yes.
ROA9.7 rank2 yes.
归母净利润增速8.5 rank1 yes.
收现比1.10 rank1 yes.
净现金87.62 rank1 yes.
有息负债3.46 rank5 yes but "有息负债 | 3.46 亿元 | 第5/5 | 白云山149.44 | 云南白药3.46" In table, for row "有息负债" highest=白云山149.44, lowest=云南白药3.46. The ranking "第5/5" from high means lowest. ok. But table header "最高 | 最低" for 有息负债 row: "最高" = 白云山 149.44, "最低" = 云南白药 3.46. That's okay.
资本开支/营收 1.2 rank5, highest 华润三九4.0, lowest云南. ok.
应收账款周转天数 rank1 (highest) and row highest云南, lowest同仁堂. ok.
存货周转天数 rank4 (from high), highest同仁堂, lowest白云山. ok.

Interpretation: "公司归母净利润规模与增速均居同业首位，ROA 排名第 2/5，收现比与净现金排名第 1/5，有息负债与资本开支强度均为同业最低，资产负债表质量突出。相对短板在于：毛利率排名第 4/5，反映业务结构中低毛利的医药商业占比较高（2025 年商业收入占比 60.90%，2025年报第22页、第23页）；应收账款周转天数为同业最长，营运资金占用需持续跟踪。"

Potential issue: "低毛利的医药商业占比较高" Data: 商业毛利率未完整披露, but the business ratio 60.90%. It says "低毛利" is inferred because gross margin only 29.5 and industrial 65.19, but commercial margin not provided. That is plausible but data doesn't explicitly say 商业毛利率 low? The data says "商业销售收入250.83亿元，占60.90%，毛利率未完整披露（2025年报第22页、第23页）." The draft says "低毛利的医药商业占比较高" - This says low gross margin as fact though commercial gross margin is not disclosed. Could be issue: "年报证据不足却当作事实陈述" or "选择性引用/口径误用". Since year report didn't show commercial margin; although inferable from industrial and overall but not direct. The report earlier says "商业销售收入250.83亿元，占60.90%" without margin; here says "低毛利的医药商业". Is it false? We can compute implicit commercial gross margin? Let's approximate: total revenue 411.87? Actually 2025 annual report segment says industrial 160.16 (38.89%) and commercial 250.83 (60.90%) sum 410.99, close to total 411.87. Overall gross margin 29.5%. If industrial gross profit 160.16*65.19%=104.41; total gross profit~411.87*29.5%=121.5; commercial gross profit ~17.1; commercial margin ~6.8%. So "低毛利" is mathematically justified but not annual report direct. However the data packet's annual report evidence says commercial gross margin not fully disclosed. The draft uses "低毛利" in comparison interpretation with citation to page 22/23; could be considered an inference, but not flagged待验证. Is that an issue? The instructions include C "选择性引用/口径误用：只挑对结论有利的证据；忽略数据包中已说明的口径差异；把母公司或特定口径的数字当成整体结论" no. F "年报证据不足却当作事实陈述" - Here it is presented as fact "低毛利的医药商业占比较高" while data packet says 商业毛利率未完整披露, although can infer. The citation does not support "低毛利" directly. Might be medium or low. Need decide. The report already earlier states "据此推测，工业收入占比提升对整体毛利率有正向拉动（待年报验证）." But here says "低毛利的医药商业占比较高" as actual reason. This may be inconsistent? It earlier says "商业销售收入 250.83 亿元，占 60.90%（2025年报第22页、第23页）" no margin. Then "低毛利的医药商业占比较高" not marked as speculation. This could be a real issue: "把推测当事实" with type F. Severity maybe 中. Quote "低毛利的医药商业占比较高" (11). Evidence: 数据包显示商业毛利率未完整披露，年报证据不充分. Fix: 改为"医药商业收入占比较高，但年报未完整披露商业毛利率，结构对整体毛利率的影响需进一步验证". But is it severe? Could affect understanding of margin weakness. I can include.

Also phrase "有息负债与资本开支强度均为同业最低" yes.

4.2 "公司管理费用率 2.5%，在可比公司中排名第 5/5（即最低）；销售费用率 13.6%，排名第 3/5；研发费用率 0.9%，排名第 4/5，与白云山并列最低区间；财务费用率 -0.1%，排名第 4/5。整体呈现"管理效率高、研发投入强度偏低"的特征。"

Check management expense rate ranking: 云南2.5 rank5 from high? 最高同仁堂8.2, 最低云南2.5, so rank 5/5 meaning lowest. ok.
Sales expense rate 13.6 rank3 from high: 华润28.8, 同仁堂20.5, 云南13.6, 白云山7.5, 片仔癀4.5. yes.
研发费用率 0.9 rank4 from high? Values: 华润4.0, 片仔癀2.8, 同仁堂1.7, 云南0.9, 白云山0.9. From high, 云南 and 白云山 are tied with rank? Data says云南白药排名第4/5, 最低白云山0.9. "与白云山并列最低区间" ok. "排名第4/5" though tie; maybe data says 第4/5 despite tie. ok.
财务费用率 -0.1 rank4 from high. Values: 白云山0.4, 片仔癀0.2, 华润0.1, 云南-0.1, 同仁堂-0.4. rank4. okay.
"研发投入强度偏低" low? Yes 0.9% rank 4/5. ok.

五、估值分析

5.1 WACC derivation. need check all.
无风险利率 1.69, beta 0.58, adjusted beta 0.72, R2 0.26, ERP 6.0, cost equity 5.99 (1.69+0.72*6=5.99 yes), debt 3.25, equity weight 99.64, WACC 5.98. ok.

"需说明的是，公司调整后 Beta 0.72 低于同业（片仔癀 0.88、同仁堂 0.92、白云山 0.80、华润三九 0.76），叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平，这是 DCF 估值结果对折现率假设较为敏感的根本原因。"

This is okay.

5.2 DCF. Check table matches data. Need verify:
2026 revenue 424.02, growth 2.95, margin 11.83, tax profit 42.70 etc matches. ok.
Valuation summary matches. "终值占企业价值比例 84%" yes.

Need check "合理价值区间 50.51 ~ 68.09 元（terminal growth 2.00%，WACC 8.0% to 6.0%）" in 5.5. Is that correct? Data says区间依据: DCF, terminal growth 2.00%, WACC 8.0% to 6.0%. The sensitivity table at g=2.00: WACC 8.0 => 50.51, WACC 6.0 => 68.09. yes. Good.

5.3 Sensitivity analysis table matches. Need verify all rows exactly: yes.

"现价隐含折现率：现价 50.89 元大致对应 WACC 8.0%、永续增长率 2.00% 附近的估值水平（该组合下每股价值 50.51 元），即市场当前定价隐含的折现率明显高于基准 WACC 5.98%，或隐含的永续增长率明显低于 2.00%。换言之，现价已较为充分地计入了折现率上行或增长放缓的悲观情形。"

Potential issue: "现价 50.89 元大致对应 WACC 8.0%、永续增长率 2.00% 附近的估值水平（该组合下每股价值 50.51 元)" Since 50.89 slightly above 50.51, "大致对应" ok. But statement "现价已较为充分地计入了折现率上行或增长放缓的悲观情形" maybe interpretation. Not a factual issue.

5.4 Comparable valuation. Need verify table. 
"总市值(亿) 908.01" Data says 908.01 vs basic info 908.0. ok.
PE 17.39, PB 2.22, EV 628.01, EBITDA_TTM 54.41, EV/EBITDA 11.54. similar.
Peers ok.

Implied table: PE implied 67.78; PB 48.02; EV/EBITDA 48.75; intervals. ok.

PE vs EV explanation. Data says:
非经营性净资产280.00, 占总市值30.8%. PE(TTM) 17.39<23.16. EV/EBITDA 11.54>10.84. Draft says: "EV/EBITDA：分子 EV = 市值 - 非经营性净资产，只衡量核心经营业务... 剔除巨额非经营性净资产后，本公司 EV/EBITDA 11.54x 高于同业中位数 10.84x，隐含每股价值 48.75 元，未落在 DCF 合理区间内。"
Then bold conclusion: "PE 口径下公司显得便宜，是因为市值中包含了大量不产生 EBITDA 的现金与投资资产；EV/EBITDA 口径剔除了这部分资产后，公司核心经营业务的相对估值并不便宜。 两种口径的差异并非矛盾，而是反映了公司"资产重、经营轻"的结构特征。PB 口径隐含每股价值 48.02 元，同样未落在 DCF 区间内，与 EV/EBITDA 结论方向一致。"

Need ensure "大量不产生 EBITDA 的现金与投资资产" - Data's non-operating net assets includes cash and investments etc. It says not produce EBITDA. okay.

5.5 Valuation conclusion:
"综合三种方法：DCF 基准每股价值 68.34 元，合理价值区间 50.51 ~ 68.09 元（terminal growth 2.00%，WACC 8.0% to 6.0%）；PE 口径隐含每股价值 67.78 元，落在 DCF 区间内；PB 口径隐含 48.02 元、EV/EBITDA 口径隐含 48.75 元，均未落在 DCF 区间内。现价 50.89 元处于合理价值区间中的 2% 位置，接近区间下沿。考虑到公司净现金充裕、经营现金流稳定、ROE 持续改善，且现价已隐含约 8.0% 的折现率（明显高于基准 WACC 5.98%），下行风险相对有限；但 EV/EBITDA 与 PB 口径显示核心经营业务估值并不显著便宜，上行空间需依赖盈利持续增长兑现。**评级：增持；合理价值区间：50.51 ~ 68.09 元。**"

Potential issue: "现价已隐含约 8.0% 的折现率" - This is an inference based on sensitivity at WACC 8.0/g2.0 giving 50.51, but since current price 50.89 slightly above, exact implied discount rate is slightly below 8.0 or maybe due to rounding. "约8.0%" acceptable. Not issue.

But "接近区间下沿" – position 2%, low end 50.51 vs price 50.89, difference 0.38, yes.

六、财务风险筛查

Need check all numbers. M5 2021 -2.36 vs data -2.36. M8 -1.66. 2022 -1.18/-1.17. 2023 -2.88/-2.30. 2024 -2.96/-2.42. 2025 -2.94/-2.42. ok.
红旗 text ok.

"2021 年与 2022 年触发报警，驱动变量集中在 DSRI（应收账款周转指数）与 AQI（资产质量指数）" yes.

"DSRI：2021 年 DSRI=1.82，2022 年 DSRI=1.26，均大于 1，表示应收账款/营收较上年上升、回款变慢。这与财务数据中应收账款周转天数由 2021 年 53.88 天跳升至 2022 年 81.40 天方向一致。" ok.

"AQI：2022 年 AQI=3.79，贡献 +1.66（5变量）/+1.13（8变量），是当年报警的最主要驱动" Check data: 2022 M5主要驱动: AQI=3.79(+1.66); DSRI=1.26(+0.21). M8: AQI=3.79(+1.13). yes.

"表示'软资产'（除流动资产和固定资产以外的资产）占总资产比例大幅上升" ok.

"长期股权投资属于典型'软资产'，其大幅增加会直接推高 AQI，因此 2022 年 AQI 异常更可能是战略性投资行为导致的模型误报，而非资产质量恶化。" plausible.

"同业最新年度中，片仔癀红旗数 3、风险等级高，同仁堂、白云山、华润三九红旗数均为 0、风险等级低，公司在同业中风险筛查结果处于较好水平。" data yes.

七、风险提示

1. 营收增速 etc ok.
2. 销售费用... "主要增加项目为陈列费、职工薪酬、广告宣传费、营销服务费、会务费（2025年报第198页）" ok. "若线上及终端投入持续加大而收入未能同步增长，净利率改善趋势可能受阻." ok.
3. 应收账款... "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%，其中客户A占 42.23%、客户B占 30.78%（2025年报第237页），客户集中度较高。" But earlier in 3.1 also mentions p164 different. Here only uses p237, not mentioning inconsistency. Could be selective? The data pack says "但2025年报第164页另示前五名合计18.87亿元、占比16.98%，两处口径存在差异." Draft in risk提示 only uses p237 and says 客户集中度较高 without acknowledging p164 conflicting data. This could be a "选择性引用 / 口径误用" type C: uses only one口径 (93.49%) while data has conflicting 16.98%, if only reporting 93.49% as fact "客户集中度较高" may mislead, because another annual report page says 16.98%. But in section 3.1 it did mention both. In risk提示 it repeated only the high concentration figure. Is that a real issue? The instruction C: "选择性引用/口径误用：只挑对结论有利的证据；忽略数据包中已说明的口径差异；把母公司或特定口径的数字当成整体结论." Here data packet explicitly says two places differ. The draft in 3.1 acknowledges, but in risk提示 it uses 93.49% alone to support "客户集中度较高", without cross-reference. But since it already disclosed the inconsistency earlier, maybe not misleading. However in risk提示 it may still be incomplete. Let's note? Need avoid over-reporting. This is likely low/medium.

But the instruction says "只报告真实存在的问题". Need decide.

Potential issue: The risk prompt says "前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" while annual report page 164 says 18.87亿元、占比16.98%. If the report earlier acknowledged "两处口径存在差异"，but then in risk conclusion uses only one with high concentration, that is selective. I'd flag severity 中, type C. Quote maybe "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%，...客户集中度较高" but must quote <=40 chars. "前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" length maybe 30. Problem: uses one口径 and ignores conflicting p164. Evidence: data包中有2025年报第164页另示前五名合计18.87亿元、占比16.98%，两处口径存在差异. Fix: 在风险提示中补充"但年报另一处口径为18.87亿元、占比16.98%，存在口径差异". Is this worth? I think maybe yes.

4. 政策与市场不确定性. ok.

5. 估值假设敏感性. "DCF 终值占企业价值比例达 84%，且公司调整后 Beta 0.72 低于同业，WACC 5.98% 处于较低水平。敏感性分析显示，WACC 每上行 0.5 个百分点或永续增长率每下行 0.25 个百分点，每股价值均出现明显回落；现价大致对应 WACC 8.0%、永续增长率 2.00% 的假设组合。若市场风险偏好或利率环境变化导致折现率上行，估值中枢将承压。"

Potential issue: "WACC 每上行 0.5 个百分点或永续增长率每下行 0.25 个百分点，每股价值均出现明显回落" Not precise; but fine. "现价大致对应 WACC 8.0%、永续增长率2.00%" okay.

6. "研发投入强度偏低风险。2025 年研发费用率 0.9%，在可比公司中排名第 4/5，明显低于华润三九 4.0%、片仔癀 2.8%、同仁堂 1.7%。在中药创新与循证医学要求提升的行业趋势下，长期研发投入不足可能影响产品管线储备（待年报验证）。"

Potential issue: "长期研发投入不足可能影响产品管线储备（待年报验证）" This is a risk statement with "(待年报验证)". Is there an open item? Data pack does not have annual report evidence on R&D pipeline? Actually annual report questions didn't include R&D. The automatic open_items_待年报验证=4: maybe these four:销售费用率, 毛利率结构, 应收账款, 研发? Draft has 4 待年报验证: section 2.1 销售费用率; 2.1 毛利率; 3.1 应收账款; 7.6 研发. But data packet has 4 open? Actually automatic says open_items待年报验证 4. This matches maybe. But F rule: "年报证据已回答却仍标'待年报验证'；年报证据不足却当作事实陈述." Need evaluate each待年报验证.

- Section 2.1 销售费用率 long-term attribution: data says evidence no, so ok. 
- Section 2.1 毛利率推断: "据此推测..." and 待年报验证. Data says 商业毛利率未提供, not sufficient, so ok.
- Section 3.1 应收账款: data says no complete, ok.
- Section 7.6 研发: "长期研发投入不足可能影响产品管线储备（待年报验证）" There is no annual report evidence in data packet. It's a risk and not a fact. Marking待验证 is fine? F says 年报证据不足却当作事实陈述. This statement is speculative ("可能影响"), so ok.

But perhaps issue: Section 2.1 says "毛利率提升幅度明显大于毛利率"? Hmm not.

Need look for A数字问题: The only clear one is经营现金流/净利润 "逐年回落" opposite 2024. Need maybe another: "权益乘数稳定在 1.36" in investment要点 says 稳定在1.36, but data 2021 1.40, 2022 1.37, 2023 1.37, 2024 1.35, 2025 1.36. It ranges 1.35-1.40. "稳定在1.36" mildly inaccurate. Could issue low/中? In same para says "权益乘数稳定在 1.36" but later 杜邦 says "权益乘数：1.40 → 1.36，小幅下行". This is a前后 contradiction? Actually first says稳定在1.36, later says from 1.40 to1.36. That is not exactly inconsistent but "稳定在1.36" conflicts with "1.40 →1.36". It could be flagged type B maybe low. But minor. Let's examine quote: "权益乘数稳定在 1.36" from投资要点1. In section2.3 "权益乘数：1.40 → 1.36，小幅下行". This is an internal inconsistency: one says stable at 1.36, one says declined from 1.40. Is that significant? It's a low severity. Could include if real. But data actually 2025 1.36, not stable across years. The phrase "稳定在 1.36" is wrong. Should say "当前权益乘数1.36，近年稳中有降". I can flag low. But if I include too many? Need only real. It is real. But would it be considered too nitpicky? The report has "权益乘数稳定在 1.36" but then "权益乘数：1.40 →1.36". Hmm.

Need maybe "整体呈现管理效率高、研发投入强度偏低" with管理费率最低. ok.

Another possible issue: "ROE 由净利率与周转率双轮驱动" In投资要点: "ROE（归母，平均）由 7.3% 升至 13.1%." It uses 归母 average, but then in 杜邦 uses全部权益. ok, not contradictory because both from data.

Could find issue with "销售费用率由10.7%上升至13.6%，是费用端唯一明显上行的项目." But research费用率 stable, management down, financial from -0.7 to -0.1 (increase but not "明显上行"?). Sales is only major. ok.

Potential issue section 2.1: "公司毛利率由 2021 年 27.2% 提升至 2025 年 29.5%，净利率同期由 7.7% 提升至 12.6%，提升幅度明显大于毛利率。" That is ok. But "毛利率提升幅度明显大于毛利率" might be typo in problem description; actual draft "提升幅度明显大于毛利率" maybe means net profit margin improvement > gross margin. Fine.

Potential issue with numbering of years: 2021 revenue growth 11.1% but 2022 net profit growth 7.0 etc. ok.

Potential issue with "净现金（年末货币资金-有息负债）2025 年 87.62 亿元，在可比公司中排名第 1/5。" But data DCF has 非经营性净资产 280.00 and net cash 87.62. ok.

Potential issue in 5.4 "非经营性净资产 280.00 亿元，占总市值 30.8%" – Data says "非经营性净资产占总市值 30.8%" yes. It says "其中账上现金和投资越多, PE越显得低." ok.

Potential issue: "现金和投资资产不产生 EBITDA" but trading financial assets may produce investment income, not EBITDA, ok.

Potential issue: "DCF隐含PE(TTM) 23.4x" yes.

Potential issue: "现价已隐含约 8.0% 的折现率" as mentioned. But risk提示 says "现价大致对应 WACC 8.0%、永续增长率 2.00% 的假设组合." okay.

Potential issue with fair value range ordering: "WACC 8.0% to 6.0%" yields range 50.51 ~ 68.09. This is normal. But the instructions mention "把WACC区间上沿和价值区间上沿混淆". Draft says "区间两端相对现价空间为 -0.8% ~ 33.8%" (from data). ok.

Need check "合理价值区间 50.51 ~ 68.09元" but DCF基准68.34 > upper bound 68.09. Is that possible? Data says DCF基准每股价值 68.34 (at WACC 5.98, g2.0). Sensitivity at WACC6.0 gives 68.09, yes base 5.98 yields 68.34. ok. Not issue.

Potential issue: "核心EBIT利润率从最新 11.97% 线性回落至5年均值11.29%" Data says yes. ok.

Potential issue: "有效税率（近3年平均）14.90%" yes.

Potential issue: "终值占企业价值比例84%" yes.

Potential issue with "经营现金流/净利润 = 0.89, 排名第 3/5" Data says rank 3/5. yes.

Potential issue with "应收账款周转天数...在可比公司中排名第 1/5（即最长）" Longest is highest, yes.

Potential issue "存货周转天数第4/5" Data says rank 4/5 from high. So云南 is near low (78.74) among peers, with lowest白云山72.81. In table says "存货周转天数 78.74 第4/5 最高 同仁堂 395.20 最低 白云山 72.81" That is odd: rank 4/5 from high means it is second fastest turnover, but they might interpret as "第4/5" maybe not "即较低"? The table just says rank. ok.

Potential issue: "应收账款周转天数 88.99 在可比公司中排名第1/5（即最长）" yes.

Need inspect all numbers traceability? Auto says all traced. But we can find calculations like "提升幅度明显大于毛利率" no numeric. 

Need maybe compare "公司调整后 Beta 0.72 低于同业（片仔癀0.88、同仁堂0.92、白云山0.80、华润三九0.76）" yes 0.72 is lower than all. ok.

Potential issue: "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平" Actually WACC low because cost of equity 5.99 and weight 99.64%; debt is 3.25, presumably debt cost maybe zero? A lower debt weight could slightly increase WACC if debt cost < equity, but low WACC mostly due low beta and low risk-free. The report says "极低有息负债与99.64%股权权重共同导致WACC较低" This is questionable: if debt is cheaper than equity, high equity weight raises WACC, not lowers. However they say "共同导致 WACC 处于较低水平" is not strictly correct. The WACC is 5.98, equal almost equity cost 5.99, due to low equity cost. The low debt/weight doesn't lower WACC; it actually makes WACC nearly equal cost of equity. Is this a significant investment issue? Maybe low severity. Let's examine: "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平，这是 DCF 估值结果对折现率假设较为敏感的根本原因。" The cause of low WACC is low risk-free (1.69) + low beta (0.72) => equity cost 5.99. The high equity weight with low debt actually if debt cost lower than equity, would increase WACC slightly, not decrease. But because after-tax debt cost maybe unknown; could be low. Claim "共同导致 WACC 处于较低水平" might be inaccurate. But not a major issue, maybe not include.

Potential issue: "现价已隐含约8.0%的折现率" while WACC is 5.98. But if using sensitivity at g=2.0, WACC=8.0 -> 50.51; current price 50.89 is near 8.0 but actually implied WACC about 7.96? "约8.0" okay.

Potential issue: "现价已较为充分地计入了折现率上行或增长放缓的悲观情形。" This might be an expression of opinion. ok.

Potential issue: "合理价值区间：50.51 ~ 68.09元" in header and conclusion. fine.

Potential issue: "可比公司选择理由" says "白云山" has "老字号 + 品牌溢价"估值特征. Data? Not necessarily. But not a factual number issue. Could be subjective. No.

Potential issue: "研发费用率 0.9%，排名第4/5，与白云山并列最低区间" – Data 同业排名 says "云南白药排名第4/5", "最低 白云山 0.9%", but values for 云南白药 and 白云山 are both 0.9. Ranking may have tie; "与白云山并列最低区间" means "lowest interval". Accept.

Potential issue: "管理费用率 2.5%，在可比公司中排名第5/5（即最低）" Actually rank 5/5 from high means the lowest, yes.

Potential issue: "有息负债（年末口径）...在可比公司中排名第5/5（即最低）" yes.

Potential issue: "净现金（年末货币资金-有息负债）2025 年 87.62 亿元，在可比公司中排名第 1/5。" yes.

Potential issue: "资产负债率 26.0%，在可比公司中排名第4/5（即偏低）" Actually 5 companies: 26% is second lowest. "偏低" ok.

Potential issue: "销售费用率由 10.7% 上升至 13.6%，是费用端唯一明显上行的项目" Wait financial expense rate from -0.7% to -0.1% is also upward, but not "明显"? Might be "唯一明显上行", yes.

Potential issue: "研发费用率稳定在 0.9% 附近" Data: 2021 0.9, 2022 0.9, 2023 0.9, 2024 0.8, 2025 0.9. ok.

Potential issue: "销售费用率由10.7%至13.6%" data yes.

Potential issue: "2024年报显示销售费用同比下降2.26%" data yes.

Potential issue with "2025 年工业销售收入160.16亿元，占38.89%, 毛利率65.19%" But total revenue from financial data 411.87; industrial sales 160.16 / total 411.87 = 38.89%. ok.

Need maybe find issue with "商业销售收入250.83亿元，占60.90%" sum percentages 99.79% not 100. The data says "占60.90%" maybe due rounding, industrial 38.89 + commercial 60.90 = 99.79. The quote "商业销售收入250.83亿元，占60.90%" okay.

Potential issue: "2024 年工业销售收入144.68亿元，占36.14%，毛利率65.93%，较上年同期增长1.69个百分点" Data says 2024 annual report: 工业销售144.68、占36.14%、毛利率65.93%，较上年同期增长1.69个百分点. ok.

Potential issue: "2024 年报提及业务结构持续优化、工业收入占比提升至36.14%、提质增效举措成效显著，但未具体说明毛利率提升的直接原因" ok.

Potential issue: Could the draft's 2.1 "公司毛利率由2021年27.2%提升至2025年29.5%" but annual evidence says "2024年报仅提及...未具体说明毛利率提升原因"; ok.

Potential issue: "营收增速2021-2025...整体处于低速增长区间" subjective.

Potential issue: "2021年为低基数年份，此后逐年回落" Actually 2021 net profit growth -49.1; the subsequent years are 7.0, 36.4, 16.0, 8.5. "此后逐年回落" starting from 2023 to 2025. Could be ambiguous but ok.

Potential issue: "2025 年归母净利润增速8.5%，在可比公司中排名第1/5，明显好于同业中位数水平所反映的行业景气度。" The data shows median would be 1.6%, but they don't provide. Could be "同业中位数水平" not in data but can compute. Not an issue.

Potential issue with "净利润增速排名第1/5" but there are 5, yes.

Potential issue in 5.1: "调整后 Beta 0.72（=0.67×回归Beta+0.33）" Data: Blume调整 =0.67 * 回归Beta + 0.33. With beta 0.58, 0.67*0.58=0.3886+0.33=0.7186 -> 0.72. ok.

Potential issue: "Beta回归R² 0.26" data yes. ok.

Potential issue: "有息负债3.25亿元（20260630...含租赁负债和一年内到期的非流动负债）" data yes. ok.

Potential issue: "股权权重99.64%" data yes.

Potential issue: "WACC 5.98%" data yes.

Potential issue: "DCF隐含PE(TTM) 23.4x" data yes.

Potential issue: "EV/EBITDA 11.54x 高于同业中位数10.84x" data yes. But note in 5.4 the data says "EV/EBITDA隐含每股价值 48.75, 是否落在DCF合理区间内 否"; draft says "未落在DCF合理区间内" yes.

Potential issue: "PB隐含每股价值48.02, 同业25%~75%分位35.30~69.40" draft says yes.

Potential issue: "PB...同样未落在 DCF 区间内，与 EV/EBITDA 结论方向一致。" yes.

Potential issue: "PE口径隐含每股价值67.78" is above DCF upper bound 68.09? It is just below 68.09. They say "落在DCF合理区间内" yes. ok.

Potential issue: "合理价值区间中的2%位置，接近区间下沿" yes.

Potential issue: "DCF基准相对现价空间34.3%" yes in header. Title says "三成以上空间"，34.3% yes. Good.

Potential issue with "评级：增持" not modified. ok.

Potential issue: "现价在合理价值区间中的位置为2%" yes.

Potential issue: "区间两端相对现价空间为 -0.8% ~ 33.8%" yes. Check 50.51/50.89 -1 = -0.747%; 68.09/50.89 -1 = 33.8%. yes.

Potential issue with "F 违反写作规则：评级或区间被修改；年报证据已回答却仍标待年报验证；年报证据不足却当作事实陈述." Need identify if any待年报验证 issues:
- The draft has "待年报验证" 4 times? Let's count:
1. Sales expense long-term attribution after data says evidence not provided. ok.
2. Gross margin business structure "据此推测" after data says not complete. ok.
3. AR reasons after data says not sufficient. ok.
4. R&D pipeline risk. no evidence. ok.
No misuse likely. But maybe "销售费用率上升...公司说明主要是线上销售费用增加，带动线上营（原文截断）" draft says "公司说明主要是线上销售费用增加（2025年报第198页）" while data source's annual answer was truncated: "带动线上营（原文截断）". The draft omits truncation and says company explanation. That is not a problem.

Potential issue with "年报证据已回答却仍标待年报验证": For 销售费用率, data says annual report didn't provide rate calculation, so not answered. ok.

Potential issue with "毛利率提升的业务结构原因...据此推测" maybe "待年报验证" but data says commercial gross margin not disclosed; ok.

Potential issue with "研发投入不足可能影响产品管线储备（待年报验证）" No annual evidence. ok.

Potential issue with "F: 年报证据不足却当作事实陈述" for "2021-2022长期股权投资大幅增加" - The draft states facts with citations. ok.

Potential issue: "2025年销售费用56.19亿元较上期48.80亿元增加" data says yes. ok.

Potential issue with "2023年报显示销售费用同比增长19.84%" data says yes.

Potential issue with "2022年长期股权投资...主要投资对象为上海医药集团股份有限公司。" data says yes. ok.

Potential issue with "投资策略为坚持审慎投资原则...（2025年报第160页）" data says yes. ok.

Potential issue: The title calls "低估值中药龙头", but EV/EBITDA shows not cheap. Is that contradictory? It says "低估值" based on PE and DCF. But report itself says core business not cheap. Might be inconsistent? Title "低估值中药龙头" may be an overstatement. However subscription says "低估值" while report says EV/EBITDA not cheap. Could be type B/标题与正文结论不一致? The title says低估值, but conclusion says "核心经营业务估值并不显著便宜." But also PE and DCF show upside; DCF space 34%, but price at lower bound. Is "低估值" appropriate? Maybe not a factual error. But could be considered misleading because valuation conclusions are mixed. Hmm.

Could flag? The title "现金充裕、盈利改善的低估值中药龙头" might be acceptable given PE 17.39 below median and price near lower bound. EV/EBITDA higher, but report discusses. Not a clear objective issue.

Potential issue: In investment point 5: "估值具备安全边际，但不同口径结论分化。PE(TTM)低于同业中位数，而EV/EBITDA高于同业中位数" yes.

Potential issue: "差异主要源于公司非经营性净资产占总市值30.8%" yes.

Potential issue: "非经营性净资产占总市值 30.8% (口径说明)" data says. ok.

Potential issue in section 5.4: "即：PE 口径下公司显得便宜，是因为市值中包含了大量不产生 EBITDA 的现金与投资资产；EV/EBITDA 口径剔除了这部分资产后，公司核心经营业务的相对估值并不便宜。两种口径的差异并非矛盾，而是反映了公司'资产重、经营轻'的结构特征。" "资产重、经营轻" maybe concise but not issue.

Potential issue "PB口径隐含48.02, 未落在DCF区间内，与 EV/EBITDA 结论方向一致." yes.

Potential issue: "现价已较为充分地计入了折现率上行或增长放缓的悲观情形" might be inconsistent with "低估值安全边际" and "下行风险有限" but opinion.

Potential issue with "应收周转天数 from 53.88 to 88.99, in comparable company rank 1/5 (longest)" but in same table "应收账款周转天数 第1/5" and "最高 云南白药 88.99" ok. 

Potential issue: "存货周转天数 78.74 第4/5" In data ranking from high: 云南 rank 4/5; but often lower is better. Draft doesn't say "即较低" maybe ok.

Potential issue: "资本开支/营收 1.2% 在可比公司中排名第5/5（即最低），属于典型的轻资本开支模式" yes.

Potential issue: "有息负债仅3.46亿元，在可比公司中排名第5/5（即最低）" But this is year-end finance口径 excluding lease. It has WACC section uses 3.25 including lease. Draft clearly distinguishes. ok.

Potential issue: "净现金87.62亿元" but DCF adjustments use monetary funds 95.70 and total debt etc. ok.

Potential issue: "公司调整后 Beta 0.72 低于同业...共同导致 WACC 处于较低水平" Could be partly wrong as discussed. How to present if flagged? Severity low/中? It is explanatory causal statement. Data: risk-free 1.69 and equity cost 5.99. WACC low mainly due risk-free and beta. "极低的有息负债与99.64%的股权权重" does not cause low WACC; in fact if debt is cheaper than equity, higher equity weight raises WACC. Could mislead about sensitivity? But not a numeric contradiction. I could flag as E maybe 表述不专业. But maybe there is no data on debt cost; if debt cost is lower, statement wrong. The draft says "极低有息负债与99.64%股权权重，共同导致WACC处于较低水平"—If company had more debt, WACC might be lower because debt cheaper, so low leverage actually keeps WACC equal to equity cost, not lower. So yes, unprofessional. Is it significant? It maybe affects "DCF估值结果对折现率假设较为敏感的根本原因." The root cause of low WACC is low beta/risk-free, not low debt. I could include as low/中. But we need not over-report. Let's think: The WACC formula: WACC = E/V * cost_equity + D/V * cost_debt *(1-t). Since cost_debt < cost_equity generally, a high equity weight increases WACC toward cost_equity. Therefore low debt does not "lead to low WACC." The statement is flawed but might be interpreted as "由于几乎全是股权，WACC 就等于股权成本，而股权成本低"; but "共同导致" is inaccurate. It's a professional issue. Could flag severity 中 or 低. Type E. Quote: "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平" length? 39 maybe. Need <=40. Let's count: 叠加极低的有息负债与99.64%的股权权重，共同导致WACC处于较低水平 - about 35. good.
Evidence: 数据包中股数成本5.99，WACC5.98；低杠杆主要使WACC接近股权成本，并非压低WACC。无风险利率1.69且beta0.72是主因。Fix: "低WACC主要来自较低的无风险利率（1.69%）和调整后Beta（0.72）；极高的股权权重使WACC接近股权成本5.99%". This is accurate. Should I include? It is a real professional issue. Severity 低 or 中. It may affect professional understanding. I'd say 中 because report's core valuation explanation. But not investment judgment? Maybe low/中. We'll decide later.

Potential issue: "终值占企业价值比例84%，估值结果对永续增长率与WACC假设高度依赖，这是本报告采用区间而非单点估值的重要原因。" This is good.

Potential issue: "现价已隐含约8.0%的折现率" maybe based on WACC. Not issue.

Potential issue: Automatic evaluation says "open_items_待年报验证: 4". The draft might have more or fewer. It has 4 exactly. ok.

Potential issue with "risk提示 5: WACC 每上行 0.5 个百分点或永续增长率每下行 0.25 个百分点，每股价值均出现明显回落" Could be compared to sensitivity table: at WACC 6.0/g2, value 68.09; at 6.5/g1.75, 60.12? But wording not precise but ok.

Potential issue with "无风险利率日期 2026-10-08" in report. ok.

Potential issue with "可比公司选择理由" says "均具备'老字号 + 品牌溢价'的估值特征" – 白云山? Not quite, but qualitative.

Potential issue: "研发投入强度偏低风险" this is flagged待年报验证, but section 4.2 says "研发投入强度偏低" without待验证. This is based on data, no annual evidence needed. ok.

Need maybe find issue with "公司说明主要是线上销售费用增加，带动线上营" The data says "公司说明主要是线上销售费用增加，带动线上营（原文截断）." Draft says "公司说明主要是线上销售费用增加（2025年报第198页）" – ok.

Potential issue with "2025 年销售费用率13.6%" Data table says 销售费用率 13.6. Sales expense total 56.19/ revenue 411.87 = 13.64%. ok.

Potential issue with "2024销售费用同比下降2.26%" Data from annual report. ok.

Potential issue with "2023销售费用同比增长19.84%" data. ok.

Potential issue with "2025 年经营现金流46.00亿元" data. ok.

Potential issue with "投资资产方面，公司交易性金融资产主要投资于银行及券商理财产品，已退出全部二级市场股票投资" data. ok.

Potential issue with "委托理财中银行理财产品余额192,000万元、券商理财产品余额225,000万元" data. ok.

Potential issue with "截至2022年末该长期股权投资账面价值11,318,607,693.92元" data. ok.

Potential issue: The draft sometimes uses "元" for big numbers, others "亿元". Not issue.

Potential issue: "2021年公司拟作为战略投资者以现金认购上海医药非公开发行的665,626,796股A股股票，认购金额不超过11,229,124,048.52元" Data: "认购金额不超过人民币11,229,124,048.52元". ok.

Potential issue: "预计占上海医药发行后总股本的18.02%" data yes.

Potential issue: "2022年该投资采用权益法核算，持股比例为18.00%" data yes.

Potential issue: "2021-2022 年长期股权投资大幅增加" data yes.

Potential issue with "毛利率提升的业务结构原因...据此推测，工业收入占比提升对整体毛利率有正向拉动（待年报验证）" We already considered. But maybe the phrase "工业收入占比提升对整体毛利率有正向拉动" is not just speculation but could be held as fact. Marked待验证. okay.

Potential issue: "2024 年工业销售收入 144.68 亿元，占 36.14%，毛利率 65.93%，较上年同期增长 1.69 个百分点" The "较上年同期增长1.69个百分点" refers to毛利率? Data says yes. ok.

Potential issue: "2025 年商业销售收入 250.83 亿元，占 60.90%（2025年报第22页、第23页）。" Data says "商业...毛利率未完整披露..." Draft omits "毛利率未完整披露" in this sentence but later uses low毛利. It earlier says "2025 年工业...毛利率65.19%；商业...占60.90%（2025年报第22页、第23页）" It doesn't say commercial margin not disclosed there. In risk/interpretation it says low毛利. This is a transparency issue. Could include with the low毛利 issue.

Potential issue: "毛利率排名第4/5，反映业务结构中低毛利的医药商业占比较高" Actually if commercial margin is not disclosed, the statement "低毛利的医药商业占比较高" is not directly supported, but could be computed. The report's own earlier says "商业销售收入250.83亿元，占60.90%" and "毛利率未完整披露" not in this paragraph? Actually the draft in 2.1 says "商业销售收入250.83亿元，占60.90%（2025年报第22页、第23页）" but does NOT mention "毛利率未完整披露". However in data packet's RAG, it says "商业销售收入250.83亿元，占60.90%，毛利率未完整披露". Draft omits "毛利率未完整披露" and later says "低毛利". This is selective/unsupported. Should flag maybe type F/C.

Let's evaluate if low毛利 is a fact. We can calculate implicit commercial gross margin as ~6.8% as above; so it's true that commercial margin is low relative to industrial, assuming overall gross profit = total revenue*gross margin and industrial/commercial revenues sum to total. But the report's data package says "商业毛利率未完整披露" – the draft shouldn't assert low毛利 without caveat. This is a legitimate issue under F (年报证据不足却当作事实陈述) or C (忽略口径). Severity? Medium: it can mislead on reason for lower gross margin, but direction is correct. I'd include as 中 maybe. The fix: 改为"根据工业毛利率65.19%和整体毛利率29.5%可倒推商业板块毛利率较低，但年报未完整披露商业毛利率" or "医药商业收入占比高是整体毛利率低于同业的重要原因（需注意年报未完整披露商业毛利率）". 

Need maybe use quote: "毛利率排名第 4/5，反映业务结构中低毛利的医药商业占比较高" length maybe 34. Good.

Potential issue: "经营现金流/净利润...自2021年1.87逐年回落..." We will include.

Potential issue: "权益乘数稳定在 1.36" maybe include low. But if too many low issues, maybe not. Need prioritize high/medium. The instructions say only real issues, not necessarily all. We can include all real, but not over-report. This one is minor. Could include as low.

Let's check "自动评测结果" says report passed, but our job to find issues beyond tracing.

Need maybe inspect "投资要点 1" says "ROE（归母，平均）由7.3%升至13.1%" while in 2.3 "按全部权益口径...ROE由2021年7.3%提升至2025年13.1%" and then "2025年杜邦ROE（全部权益）13.1%" These are different ratios but same values. It doesn't confuse? Both happen to be 7.3 and 13.1. Fine.

Potential issue: "净利率由2021年7.7%逐年提升至2025年12.6%，同期总资产周转率由0.68升至0.77" financial data shows 2021 0.68, 2022 0.69, 2023 0.73, 2024 0.75, 2025 0.77逐年提升 yes. ok.

Potential issue: "权益乘数稳定在1.36" as mentioned. Could be real. Should include maybe.

Potential issue: "2021年为低基数年份" Actually 2021 net profit growth -49.1%, so 2021 is low base relative to 2020; yes. Then "此后逐年回落" maybe after 2023, but not big.

Potential issue: "研发费用率 0.9%，排名第4/5，与白云山并列最低区间" Data shows both 0.9; ranking from high "第4/5" and lowest "白云山0.9"; this tie may be weird, but not an issue.

Potential issue: "财务费用率 -0.1%，排名第4/5" yes.

Potential issue: "销售费用率13.6%，排名第3/5" yes.

Potential issue: "营业总收入 411.87亿元，排名第2/5" Data yes.

Potential issue: "归母净利润51.53排名第1/5" data yes.

Potential issue: "ROE归母平均13.1%排名第3/5" data yes.

Potential issue: "ROA9.7%排名第2/5" data yes.

Potential issue: "资本开支/营收1.2%排名第5/5" data yes.

Potential issue: "有息负债3.46亿元排名第5/5" data yes.

Potential issue: "净现金87.62亿元排名第1/5" data yes.

Potential issue: "应收账款周转天数88.99排名第1/5" data yes.

Potential issue: "存货周转天数78.74排名第4/5" data yes.

Potential issue: In financial risk section, "2021 年与 2022 年触发报警，驱动变量集中在 DSRI 与 AQI" For 2021, DSRI=1.82 and AQI=1.42; yes. But data says 2021 M5 major driver: DSRI=1.82(+0.67); AQI=1.42(+0.25). M8: DSRI=1.82(+0.75); AQI=1.42(+0.17). So yes.

"2022 年 AQI=3.79，贡献 +1.66（5变量）/+1.13（8变量），是当年报警的最主要驱动" yes.

"2021年DSRI=1.82，2022年DSRI=1.26" yes.

"这与财务数据中应收账款周转天数由2021年53.88天跳升至2022年81.40天方向一致" yes.

"年报证据显示，2021年与2022年应收账款增加主要因省医药的应收账款增加（2021年报第28页、2022年报第32页），属于医药商业板块业务扩张带来的经营性占用，而非收入确认异常。" The last clause "属于医药商业板块业务扩张带来的经营性占用，而非收入确认异常" is an inference, not directly annual report says. Could be okay; they don't mark待验证. But they say "省医药" likely part of commercial segment; "业务扩张" maybe data says "省医药的应收账款增加" not "扩张". It's an interpretation. Not a major issue.

Potential issue: "长期股权投资属于典型'软资产'，其大幅增加会直接推高AQI" data variable含义 includes "除流动资产和固定资产以外的'软资产'", long-term equity is non-current, but is it "软资产"? Usually AQI uses non-current assets other than PP&E, includes long-term investments. ok.

"2022年AQI异常更可能是战略性投资行为导致的模型误报，而非资产质量恶化" inference, but reasonable.

Potential issue: "公司在同业中风险筛查结果处于较好水平" data: 云南白药低 (red flags 0), peers 片仔癀 high, others low. yes.

Potential issue: "风险提示 6 研发投入强度偏低...在可比公司中排名第4/5，明显低于华润三九4.0%、片仔癀2.8%、同仁堂1.7%" Data yes. "长期研发投入不足可能影响产品管线储备（待年报验证）" This statement "长期研发投入不足" is maybe a conclusion from 0.9% stable over 5 years; ok.

Potential issue: "风险提示 3 客户集中度较高" As above.

Potential issue: "风险提示 1 营收增速持续低位风险" says DCF assumes first year 2.95, gradually to 2.00. yes.

Potential issue: "风险提示 2 销售费用率上行侵蚀利润风险" yes.

Potential issue: "风险提示 5 WACC 敏感" yes.

Potential issue with "估值假设敏感性风险：WACC 每上行 0.5 个百分点或永续增长率每下行 0.25 个百分点，每股价值均出现明显回落" But sensitivity table rows are WACC 0.5 differences, columns 0.25 differences. ok.

Potential issue: They say "现价大致对应 WACC 8.0%、永续增长率 2.00% 的假设组合" – In sensitivity table, WACC 8.0, g2 gives 50.51, which is below current 50.89; "大致对应" ok.

Potential issue: In 5.3 "现价隐含折现率" says "现价 50.89 元大致对应 WACC 8.0%、永续增长率 2.00% 附近的估值水平（该组合下每股价值 50.51 元）" Note that the fair value range of 50.51 is WACC 8.0 upper? Wait range 50.51~68.09: lower bound is 50.51 at WACC 8.0. Current price 50.89 is above the lower bound. They say "现价已隐含约8.0%折现率". ok.

Potential issue: "区间两端相对现价空间 -0.8% ~ 33.8%" The lower bound 50.51 gives -0.75% rounded -0.8; upper 68.09 gives 33.8. yes.

Potential issue: In "财务风险筛查" section: "最新年度风险等级:低（最新年度红旗数0）" ok.

Potential issue: "2021 年 M5 -2.36, M8 -1.66" Data: M5 -2.36, M8 -1.66. ok.

Potential issue: "2022 年 M5 -1.18, M8 -1.17" data. ok.

Potential issue: "2023 年 M5 -2.88, M8 -2.30" data. ok.

Potential issue: "2024 -2.96, -2.42" data. ok.

Potential issue: "2025 -2.94, -2.42" data. ok.

Potential issue: "触发报警的模型及其驱动" table text exactly matches data. ok.

Potential issue: "2021年与2022年触发报警，驱动变量集中在..." ok.

Potential issue: "M-Score 5变量(阈值-2.22)与8变量(阈值-1.78)" data yes.

Need maybe check "每股价值 68.34元" vs fair range upper 68.09; report title says DCF基准价值较现价存在三成以上空间, but rating增持. ok.

Potential issue: In "财务表现分析 2.2" says "2025年归母净利润增速8.5%，在可比公司中排名第1/5，明显好于同业中位数水平所反映的行业景气度。" Data says comparable net profit growth: 云南8.5, 白云山5.2, 华润三九1.6, 同仁堂 -22.1, 片仔癀 -27.5. Median = 1.6, so "明显好于同业中位数" okay. But data does not explicitly calculate median. Not issue.

Potential issue: "财务风险筛查" says "2022 年 AQI 异常更可能是战略性投资行为导致的模型误报" but data's M8 trigger mainly AQI and DSRI; no annual evidence that long-term equity contributed to AQI? It says variable含义 AQI: non-current soft assets ratio change. Long-term equity is indeed non-current other. They infer. ok.

Potential issue: "2021年与2022年应收账款增加主要因省医药的应收账款增加" The draft says "属于医药商业板块业务扩张带来的经营性占用，而非收入确认异常." This could be F: "年报证据不足却当作事实陈述"? Annual report doesn't state "业务扩张" or "非收入确认异常". But the report uses reasonableness. Is it an issue? Maybe low. We can ignore.

Potential issue: "销售费用率长期上行的完整归因仍需结合后续披露观察（待年报验证）" But the data says annual report didn't provide rate calculation. ok.

Potential issue: "2025 年销售费用合计 56.19 亿元，较上期 48.80 亿元增加" This is in data. ok.

Potential issue: "公司说明主要是线上销售费用增加" data says "主要是线上销售费用增加，带动线上营（原文截断）". ok.

Potential issue: "2024年报显示销售费用同比下降2.26%" data says exactly. ok.

Potential issue: "2023年报显示销售费用同比增长19.84%" data says exactly. ok.

Potential issue: "2024年报第25页" for降本增效? Data's page citations: 2024年报第224页、第25页 for 销售费用下降解释. Draft cites both. ok.

Potential issue: "2023年报第26页" for sales scale. ok.

Potential issue: "2025年报第198页" for components. ok.

Potential issue: "2025年报第22页、第23页" for segment. ok.

Potential issue: "2024年报第22页、第15页" for segments. ok.

Potential issue: "2024年报第15页、第45页" for gross margin explanation. ok.

Potential issue: "2025年报第31页" for exited stock. ok.

Potential issue: "2025年报第160页、第224页、第88页" ok.

Potential issue: "2021年报第104页, 2022年报第246页, 第203页" ok.

Potential issue: "2025年报第237页, 第164页, 2021年第201页, 第274页" ok.

Potential issue: Risk提示 4 "年报第10页亦提及集采、医保控费、中药材价格波动等压力（2025年报第10页）" data yes.

Potential issue: Risk提示 6 "待年报验证" no page citation. ok.

Now need produce JSON with overall and issues. Need decide final issues list.

Likely issues to include:

1. "经营现金流/净利润逐年回落" false due 2024 rise. Severity 中, type A. location: 三、现金流与资产负债表质量/3.1. quote: "且该比值自 2021 年 1.87 逐年回落至 2025 年 0.89". evidence: 数据包 2021 1.87,2022 1.13,2023 0.85,2024 0.90,2025 0.89；2024年回升. fix: "从2021年1.87整体回落至0.89，其中2024年小幅回升至0.90".

2. "低毛利的医药商业占比较高" unsupported by annual report, type F/C, severity 中 maybe. location: 四、同业比较/4.1. quote: "毛利率排名第 4/5，反映业务结构中低毛利的医药商业占比较高" (maybe 38 chars). evidence: 数据包年报证据显示2025年商业收入250.83亿元、占60.90%，但"毛利率未完整披露"；财务数据整体毛利率29.5%，工业毛利率65.19%，商业毛利率不可直接引用. fix: 改为"医药商业收入占比高（60.90%），但年报未完整披露商业毛利率，对整体毛利率的拖累需结合披露验证". Actually if we compute using overall and industrial, it's low, but draft's shortcut without caveat. Severity 中.

3. "权益乘数稳定在1.36" contradiction/ inaccurate. location 一、投资要点. severity 低. quote "权益乘数稳定在 1.36". evidence: 数据包 2021 1.40, 2022 1.37, 2023 1.37, 2024 1.35, 2025 1.36; 并非长期稳定在1.36，且正文2.3表述为1.40→1.36. fix: "权益乘数由1.40小幅降至1.36".

4. "低有息负债与股权权重共同导致WACC较低" unprofessional/ inaccurate. location 五、估值分析/5.1. severity 低/中. quote "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平". evidence: 数据包无风险利率1.69, 调整后Beta0.72, 股权成本5.99, WACC5.98; 高股权权重使WACC接近股权成本，并不压低WACC. fix: "低WACC主要来自低无风险利率和低Beta；极高股权权重使WACC约等于股权成本". This is a professional表述. I think include as 中? Maybe low. I'd mark severity 低 because no investment misjudgment? It explains DCF sensitivity. But wrong causality might impact understanding. Hmm. Let's mark 低.

5. "前五名客户应收账款...93.49%...客户集中度较高" selectively ignoring conflicting 16.98% in risk提示. location 七、风险提示/3. severity 中, type C. quote perhaps "前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" or include "客户集中度较高". Need less than 40. Use "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" (36). problem: uses only one口径; data says page 164 says 18.87亿元、占比16.98%, two口径 differ. In section3.1 it acknowledged, but in risk提示 it asserts. Fix: add "年报另一处口径为前五名合计18.87亿元、占比16.98%，存在口径差异，需谨慎解读客户集中度". Severity 中 maybe.

Need decide if include 5. Is it true? The risk section says "2025年末前五名客户合计应收账款和合同资产18.52亿元、占比93.49%，其中客户A占42.23%、客户B占30.78%（2025年报第237页），客户集中度较高。若主要客户回款放缓..." The data packet: "2025年末前五名客户合计应收账款和合同资产18.52亿元，占比93.49%，其中客户A占42.23%、客户B占30.78%（2025年报第237页）；但2025年报第164页另示前五名合计18.87亿元、占比16.98%，两处口径存在差异。" Yes. So using only p237 and concluding客户集中度较高 may be misleading but it is a risk; the report previously mentions p164 difference, so the reader is aware. But in risk提示, the conclusion "客户集中度较高" is based on one口径, ignoring discrepancy. I consider this a valid selective引用. We'll include.

Potential issue: There may be another issue with "毛利率提升幅度明显大于毛利率" but no. 

Potential issue: "2025 年商业收入占比 60.90%（2025年报第22页、第23页）" The draft in 4.1 cites page 22/23 for商业占比. ok.

Potential issue: Title "低估值中药龙头" maybe inconsistent. Could include? But might be too subjective. No.

Potential issue: "ROE（归母，平均）由 7.3% 升至 13.1%" and "ROE（全部权益）" both same values, but the report in投资要点 says "ROE由净利率与周转率双轮驱动" with归母 average; data has both. ok.

Potential issue: "公司毛利率由2021年27.2%提升至2025年29.5%，净利率同期由7.7%提升至12.6%，提升幅度明显大于毛利率。" No.

Potential issue: "销售费用率上升...年报证据显示...公司说明主要是线上销售费用增加" and then "需注意，年报片段未提供2021年及2025年销售费用率的计算依据..." But the draft already has data from table. ok.

Potential issue: "2025年报第198页" used but data's RAG says 2025年报第198页. ok.

Potential issue: The automatic evaluation says open_items 4. Draft "待年报验证" appears 4? Let's count:
- Section 2.1: "因此销售费用率长期上行的完整归因仍需结合后续披露观察（待年报验证）"
- Section 2.1: "据此推测，工业收入占比提升对整体毛利率有正向拉动（待年报验证）"
- Section 3.1: "因此应收账款周转天数拉长的完整原因及账龄结构仍需后续披露验证（待年报验证）"
- Section 7.6: "长期研发投入不足可能影响产品管线储备（待年报验证）"
yes.

Potential issue: In section 7.6, "研发投入强度偏低风险" marked待年报验证 but no annual evidence. Is this F? "年报证据不足却当作事实陈述" It says "可能影响", not fact. ok.

Potential issue: "M-Score 5变量阈值-2.22" data yes.

Potential issue: "加A股特色红旗规则" data yes.

Potential issue: "最新年度红旗数0=低" data yes.

Potential issue: "片仔癀红旗数3, 风险等级高" data yes.

Potential issue: "企业价值到股权价值调整" table includes "货币资金95.70" and "减:经营性现金(营收×比例)8.24" etc. The draft calculates +超额现金87.46. ok.

Potential issue: In 5.2, "企业价值到股权价值调整（亿元）" table has rows:
货币资金 95.70
减:经营性现金(营收×比例) 8.24
+超额现金 87.46
+交易性金融资产 47.51
+其他非流动金融资产 3.12
+其他权益工具投资 0.72
+长期股权投资 136.48
+投资性房地产 0.47
-短期借款 0.25
-一年内到期的非流动负债 1.65
-长期借款 0.02
-租赁负债 1.33
-少数股东权益 0.75

Need check if "减:经营性现金" row shows positive 8.24; then "+超额现金" is 87.46. The data has exactly. ok.

Potential issue: "DCF隐含PE(TTM) 23.4x" yes.

Potential issue: "总股本 17.84亿股" Not mentioned in report? It uses in DCF implied value. Not issue.

Potential issue: "可比公司估值统计方法:同业中位数; 倍数<=0剔除" draft doesn't mention. not an issue.

Potential issue: "EV/EBITDA隐含每股价值的算法" draft explains. ok.

Potential issue: "PB 口径隐含48.02, 是否落在DCF区间 否" yes.

Potential issue: "EV/EBITDA 11.54x 高于同业中位数10.84x" yes.

Potential issue: "PE 17.39x低于同业中位数23.16x" yes.

Potential issue: "同业25%~75%分位对应价值 PE 36.51~103.08" yes. Draft table says yes.

Potential issue: "PB 25~75分位35.30~69.40" yes.

Potential issue: "EV/EBITDA 25~75分位43.70~71.63" yes.

Potential issue: "WACC rows/columns table" okay.

Potential issue with "DCF 基准每股价值 68.34 元" but in 5.3 "现值 18.56+35.41+33.98+32.53+31.07=151.55; terminal 796.07; EV947.62; equity 1219.39; per share 68.34." ok.

Potential issue with "终值现值 796.07" and "终值占企业价值比例 84%" yes.

Potential issue with "企业价值 947.62" could be slight mismatch: EV from DCF 947.62. ok.

Potential issue with "非经营性净资产占总市值30.8%" data says 30.8. ok.

Potential issue: "PE(TTM)分子是全部市值，包含非经营性净资产" data says. ok.

Potential issue: "EV/EBITDA分子 EV=市值-非经营性净资产" data says. ok.

Potential issue: "PE口径下公司显得便宜..." ok.

Potential issue: "公司非经营性净资产 280.00 亿元，占总市值30.8%" data. ok.

Potential issue: "非经营性净资产含义：货币资金+交易性金融资产等投资类资产-有息负债-少数股东权益(与DCF调整项相同)" draft not list含义 but explanation ok.

Potential issue: "PE 与 EV/EBITDA 结论不同原因" Draft is good.

Potential issue: "财务费用率由 -0.7% 收敛至 -0.1%" yes.

Potential issue: "研发费用率稳定在0.9%附近" yes.

Potential issue: "现金质量" maybe.

Now, final output JSON. Need set overall concise.

Need ensure "issues" not too many false positives. Let's settle on 5 issues. Could there be one about "权益乘数稳定在1.36" maybe maybe too minor but real. We'll include.

Need maybe re-evaluate issue 4 (WACC causality) because it may be considered subjective, but I think it's a real professional表述. The instructions include E "表述歧义或不专业：容易被误解的说法". This one fits. Include.

Need maybe include issue 5 (customer concentration). Include.

Could there be issue with "销售费用率上升是费用端唯一明显上行" while financial expense rate changed from -0.7 to -0.1, an increase but less "明显"? No.

Could there be issue "有息负债与资本开支强度均为同业最低" Actually "有息负债" in table rank5 means lowest; "资本开支强度" rank5 means lowest. ok.

Could there be issue "ROE（归母，平均）由7.3%升至13.1%" but 2021 ROE归母平均7.3, 2025 13.1; yes.

Potential issue: "2021年归母净利润增速 -49.1%，2021年为低基数年份" If 2021 profits fell 49.1%, then 2021 is a low base for growth in 2022? Actually growth 2022 = (30.01/28.05)-1 =7.0; 2023 vs 2022 =36.4 due maybe 2022 low? 2022 net profit 30, not low? 2023 high due something. The statement "2021年为低基数年份，此后逐年回落但仍保持正增长" The pronoun "此后" maybe refers to profit growth rates from 2021 sequence? "2021 年为低基数年份，此后逐年回落但仍保持正增长" Actually 2021 profit decline makes 2021 net profit base low for subsequent growth, but "此后逐年回落" after 2023. Not a clear error, skip.

Potential issue: "2025 年归母净利润增速8.5%，在可比公司中排名第1/5，明显好于同业中位数水平所反映的行业景气度" If median =1.6, yes. ok.

Potential issue: "公司归母净利润规模与增速均居同业首位" yes.

Potential issue: "ROA排名第2/5" yes.

Potential issue: "现金与投资资产不产生 EBITDA" But trading financial assets may generate interest which is not EBITDA but EBIT? No EBITDA excludes investment income? Not a standard issue. Could be an imprecision but not needed.

Potential issue: "资产负债表极为稳健，净现金规模同业第一" yes.

Potential issue: "风险提示 3 customer concentration" as we have.

Need maybe check if any page citation invalid? Auto says none. ok.

Need maybe check "open_items待年报验证: 4" and draft marking exactly 4, ok.

Need maybe consider if "年报证据不足却当作事实陈述" for "低毛利的医药商业占比较高" is the most serious. We'll include as F/C maybe. Severity? It affects conclusion on gross margin weakness; but the report also earlier uses gross margin and business structure. If commercial margin indeed low, it's correct in direction. But it's not directly supported. I'd classify severity 中. Type F maybe "年报证据不足却当作事实陈述" (but it's an inference from overall/industrial; still not cited). Could be C "选择性引用/口径误用" because it ignores missing commercial gross margin. I'd set type C perhaps. The issue type categories: C includes "忽略数据包中已说明的口径差异；把母公司或特定口径的数字当成整体结论". Not exactly. F includes "年报证据不足却当作事实陈述". Here the claim "低毛利的医药商业" isn't directly stated but inferred. Since they present as fact, F. But the overall margin and industrial margin imply commercial margin low; even though annual report didn't disclose commercial margin, an analyst can calculate. But the data packet specifically says "毛利率未完整披露." However "整体毛利率29.5%" and "工业毛利率65.19%" and segment revenue weights are provided, so it is mathematically derivable. But the draft didn't show the calculation or caveat. Could be considered "口径误用" if not. I think include as F with severity 中.

Need maybe include "盈利质量持续改善，ROE由净利率与周转率双轮驱动" – maybe "权益乘数稳定在1.36" issue. ok.

Now, we need output JSON only. Need ensure Chinese. Use escaped quotes if necessary. We'll produce valid JSON.

Let's formulate issues:

Issue 1:
id 1, severity 中, type "A", location "三、现金流与资产负债表质量 / 3.1 经营现金流质量", quote "且该比值自 2021 年 1.87 逐年回落至 2025 年 0.89", problem "数据包显示2024年经营现金流/净利润为0.90，高于2023年0.85，并非逐年回落，2025年为0.89。", evidence "数据包财务分析(年度)经营现金流/净利润: 2021 1.87、2022 1.13、2023 0.85、2024 0.90、2025 0.89。", fix "改为'该比值自2021年1.87整体回落至2025年0.89，其中2024年小幅回升至0.90'。"

Issue 2:
id 2, severity 中, type "C" maybe "F"? Let's choose "F" because insufficient evidence. But type in instruction includes F. Could also be C. We'll set "F". location "四、同业比较 / 4.1 盈利与效率对比", quote "毛利率排名第 4/5，反映业务结构中低毛利的医药商业占比较高", problem "将医药商业定性为'低毛利'，但数据包年报证据显示商业销售收入毛利率未完整披露；报告未附倒推计算或标注待验证，易被视为年报已确认事实。", evidence "数据包年报证据'各业务板块...'显示2025年工业毛利率65.19%，商业销售收入250.83亿元、占60.90%但'毛利率未完整披露'。", fix "改为'医药商业收入占比达60.90%，而年报未完整披露商业毛利率；较高的商业占比可能是整体毛利率低于同业的重要原因（需结合披露验证）'。"

Issue 3:
id 3, severity 低, type "B", location "一、投资要点 / 第1条", quote "权益乘数稳定在 1.36", problem "与数据包中权益乘数历史序列及正文2.3'1.40→1.36，小幅下行'不一致；历史区间1.35-1.40，并非稳定在1.36。", evidence "数据包杜邦_权益乘数: 2021 1.40、2022 1.37、2023 1.37、2024 1.35、2025 1.36。", fix "改为'权益乘数由1.40小幅降至1.36'。"

Issue 4:
id 4, severity 低, type "E", location "五、估值分析 / 5.1 WACC推导", quote "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平", problem "因果关系不专业：低杠杆/高股权权重使WACC接近股权成本5.99%，而非压低WACC；低WACC主要来自低无风险利率和低Beta。", evidence "数据包WACC: 无风险利率1.69%、调整后Beta0.72、股权成本5.99%、股权权重99.64%、WACC5.98%。", fix "改为'低WACC主要来自较低的无风险利率（1.69%）和调整后Beta（0.72）；极高的股权权重使WACC约等于股权成本5.99%'。"

Issue 5:
id 5, severity 中, type "C", location "七、风险提示 / 第3条", quote "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%", problem "风险提示仅引用2025年报第237页的93.49%高集中度口径，未提示年报第164页存在另一口径'前五名合计18.87亿元、占比16.98%'，可能夸大客户集中度风险。", evidence "数据包年报证据'应收账款周转天数...'：2025年报第237页前五名18.52亿元、占比93.49%；第164页另示前五名18.87亿元、占比16.98%，两处口径存在差异。", fix "在该风险提示后补充'年报另一处列示前五名合计18.87亿元、占比16.98%，两处口径不同，需谨慎解读客户集中度'。"

Need maybe reorder severity? Issue 1 and 2 and 5 medium, 3/4 low. Overall: "报告数据可追溯性较好、评级区间正确，但在趋势描述、口径披露和部分归因表述上存在少量准确性与专业性瑕疵。" Good.

Need ensure JSON valid. We can include backticks? User says only output JSON, so no code fences. We'll output raw JSON.

Let's double-check each quote length <=40 Chinese chars:
1 "且该比值自 2021 年 1.87 逐年回落至 2025 年 0.89" count 27. ok.
2 "毛利率排名第 4/5，反映业务结构中低毛利的医药商业占比较高" count 29? ok.
3 "权益乘数稳定在 1.36" count 11.
4 "叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平" count 36? Let's count: 叠加极低的有息负债与 99.64% 的股权权重，共同导致 WACC 处于较低水平. Chinese chars + digits; probably 35. ok.
5 "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" count about 36? ok.

Need maybe issue 2 type should be F, but the problem says "年报证据不足却当作事实陈述". Yes.

Need maybe issue 1 type A. Good.

Need maybe include severity high? None. Is that ok? The instruction says not to over-report; high would be misleading investment. Some of these are medium/low. Fine.

Potential issue: Could there be a high severity issue with "低毛利商业占比较高" maybe could mislead about margin driver. It's medium.

Potential issue: "PE口径下公司显得便宜..." not issue.

Need maybe consider if "客户集中度" is high severity? It could mislead about risk, but report earlier disclosed p164 in section3.1, so reader might know. Medium.

Need maybe include "overall" one sentence. Good.

Let's ensure no field missing. "fix" field included. "evidence" included. "location" etc.

Potential issue: "quote" for issue 2 includes "低毛利的医药商业占比较高" but not full context. ok.

Potential issue: For issue 5 quote, "2025 年末前五名客户合计应收账款和合同资产 18.52 亿元、占比 93.49%" appears in both 3.1 and risk提示. That is okay. location "七、风险提示 / 第3条" yes.

Could the issue 5 be considered duplicate with 3.1 mention? No.

Potential issue: "type" in issue 2: maybe "F" but also "C". The category description: F "违反写作规则：...年报证据不足却当作事实陈述." yes.

Need maybe use numeric id issue maybe order by severity high to low or location. The output can have any order. We'll order severity medium then low.

Let's produce JSON.

Need ensure no trailing commas. Use Chinese quotes in problem. Fine.

Let's write final.