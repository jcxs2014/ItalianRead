---
title: ItalianRead — 意大利语精读
description: 意大利语精读文章列表
---

# ItalianRead — 意大利语精读

中文母语者用高品质意大利语来源做**逐句意语精读**的个人知识库。
目标是"从看中文翻译过渡到直接读懂意大利语原文"。

## 内容统计

| 来源           | 篇数 | 难度     |
| -------------- | ---- | -------- |
| doppiozero     | 4    | B2-C1   |
| Il Post        | 8    | B1-B2   |
| Contropiano    | 7    | B2-C1   |
| Internazionale  | 4    | B2-C1   |
| racconti       | 205  | A2-C1   |
| **总计**           | **228** |          |

## 精读格式

- **文章精读**：概览 → 逐句精读 → 词汇分级 → 长难句 → 总结 → 可迁移表达
- **故事精读**：chunk分段（原文→翻译→注释）+ 词汇表 + 固定表达 + 文化注释 + 文学手法 + 主题探讨 + 精读笔记
- **新闻精读**：800-1000词核心段落 + 完整精读结构

## 每日工作流

1. **抓文**：Calibre Fetch News 或 `python3 scripts/fetch_doppiozero.py`
2. **提取**：`ebook-convert "news/xxx.epub" /tmp/xxx.txt`
3. **选文**：选 800-1000 词核心段落，B1-C1 难度
4. **精读**：逐句分析，原句 / 自然中文 / 句子结构 / 动词变位 / 关键词 / 表达方式
5. **本地预览**：`./serve.sh`

## 本地预览

```bash
./serve.sh          # 启动 http://localhost:8080
./serve.sh build    # 仅构建
```

## 部署（Cloudflare Pages）

- Build command: `bash build.sh`
- Build output: `site/public`
- 环境变量: `NODE_VERSION=22`（由根目录 `.nvmrc` 自动设置）
