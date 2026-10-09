---
name: report_writer
description: 报告撰写与多智能体审稿。writer.py 把各技能结果组装成事实数据包并由大模型写初稿；review.py 由审稿Agent（deepseek-v4-pro，开启思考）找问题、修订Agent（deepseek-flash）改稿，输出定稿。
---

# 技能 6：报告撰写 + 审稿 / 修订

## 文件
| 脚本 | 角色 | 模型 |
|---|---|---|
| `writer.py` | 写稿人：事实数据包 → 初稿 | deepseek-flash，**关闭思考** |
| `review.py` | 审稿人：对照数据包找矛盾、选择性引用、比较错误等 | deepseek-v4-pro，**开启思考** |
| `review.py` | 修订人：逐条修改 → 定稿 | deepseek-flash，关闭思考 |

设置在 `config/report.toml`（评级规则、模型、温度、token 上限）。

## 输出（`reports/`）
`{code}_facts.json`（事实数据包）、`{code}_prompt.md`、`{code}_draft.md`、`{code}_review.json`、`{code}_review_thinking.md`、`{code}_final.md`

## 运行
```
python skills/report_writer/writer.py --dry-run   # 只生成数据包和提示词
python skills/report_writer/writer.py
python skills/report_writer/review.py             # 审稿 + 修订
python skills/report_writer/review.py --verify    # 复查定稿
```

## 关键设计
1. **Python 计算并格式化所有数字**，模型只负责组织语言（"11.97%"是字符串，照抄即可）。
2. **评级由规则决定**：现价在合理区间中的位置（<0 买入，下1/3 增持，中间 中性，上1/3 减持，>1 卖出）。
3. **把判断前移到 Python**：同业排名、PE 与 EV/EBITDA 口径说明、触发报警的模型及驱动，都预先算好放进数据包。v1 的 4 处比较错误因此在 v2 全部消除。
4. **年报证据带页码进入数据包**：v3 新增 30+ 处年报引用，"待年报验证"只保留在证据确实不足的地方。
5. **思考模式按需开关**：写作关闭（推理已由 Python 完成；开启时思考耗尽输出额度导致空报告），审稿开启（需要真正推理）。
