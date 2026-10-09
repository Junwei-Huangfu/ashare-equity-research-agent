---
name: annual_report_rag
description: 年报阅读（RAG）。从巨潮资讯下载年报PDF，切成带页码的文本块，用jieba搜索模式分词+BM25检索，并让大模型基于证据回答研究问题、标注页码、核验引用。需要用年报原文验证定性判断时调用。
---

# 技能 5：年报阅读（RAG）

## 文件
| 脚本 | 作用 |
|---|---|
| `fetch_reports.py` | 从巨潮资讯（AKShare 列表 + static.cninfo.com.cn PDF）下载全文年报 |
| `index.py` | PDF → 清洗 → 400字切块（重叠100字，保留年份/页码/章节）→ BM25 检索 |
| `qa.py` | 多查询检索 → 证据 → 大模型回答（带页码）→ 引用核验 |

问题与检索词在 `config/rag_questions.toml`。

## 输出
- `data/raw/annual_reports/{code}_{year}.pdf`、`data/processed/rag/`（均被 git 忽略，可重建）
- `reports/{code}_annual_report_qa.json / .md`

## 运行
```
python skills/annual_report_rag/fetch_reports.py
python skills/annual_report_rag/index.py "销售费用 增加 原因" 2025   # 单独测试检索
python skills/annual_report_rag/qa.py --dry-run                      # 只检索，不花钱
python skills/annual_report_rag/qa.py
```

## 关键设计
- **BM25 而非向量检索**：DeepSeek 官方 API 未提供 embedding 模型；年报术语高度标准化，关键词检索效果好。检索函数独立，可替换。
- **jieba 搜索模式**：精确模式下"上海医药"与"上海医药集团"切词不一致导致检索失败，改用搜索模式解决。
- **多查询召回 + 会计政策降权 + 按页去重**：解决模板化会计政策文字得分虚高的问题。
- **引用核验**：模型引用的每个页码必须在提供给它的证据中，否则标为无效引用。
- **诚实标注**：证据不足时 `sufficient=false`，不让模型硬答。
