# ItalianRead — 意大利语精读库

中文母语者用高品质意大利语来源做**逐句意语精读**的个人知识库。
目标是"从看中文翻译过渡到直接读懂意大利语原文"。

## 目录结构

```
~/Documents/Works/ItalianRead/
├── README.md              ← 本文件（唯一权威项目文档）
├── AGENTS.md              ← 本工作区 agent 操作手册
├── COLLABORATION.md       ← 协作消息板
├── .memory/               ← 本机工作记忆
│   └── ItalianRead_MEMORY.md
├── .gitignore             ← 预留（未来建 git 时用）
├── doppiozero/            ← 文学/文化（难度 B2-C1）
├── lastampa/              ← 新闻（难度 B1-B2）
└── lescienze/            ← 科学/文化（难度 B1-B2）
```

## 来源

| 来源               | RSS URL                                    | 类别     | 难度  |
| ------------------ | ------------------------------------------ | -------- | ------ |
| **doppiozero**     | `doppiozero.com/articoli-doppiozero/rss.xml` | 文学/文化 | B2-C1 |
| **La Stampa**      | `lastampa.it/rss`                          | 新闻     | B1-B2 |
| **Le Scienze**     | `lescienze.it/rss`                         | 科学/文化 | B1-B2 |

## 每日工作流

> **节奏**：手动触发，用户说"抓文" → 抓文 + 自动选 3-4 篇 + 开精读。

1. **抓文**（手动触发）
   ```bash
   cd ~/Documents/Works/ItalianRead
   python3 doppiozero/fetch_doppiozero.py   # 或 lastampa/fetch_lastampa.py 等
   ```

2. **自动选 3-4 篇**（AI 完成）
   - 长度适中（约 500–2500 词）
   - 题材多样，避免撞主题
   - 敏感剔除：政治/宗教极端/暴力 → 跳过
   - **语言密度**：长难句多、可读性高者优先
   - 去重：检查之前已抓取的 URL

3. **精读**（交给 AI 助手）
   - 逐句：原句 / 自然中文 / 句子结构 / 关键词 / 地道表达 / "为什么这样写"
   - 重点标注**动词变位**、**名词单复数**、**前置词搭配**
   - 词汇分级标注 A1/A2/B1/B2 级别
   - 段落逻辑分析；长难句专项
   - 文末总结：核心词汇 / 表达 / 语法 / 长难句 / 写作技巧 / 可迁移表达

4. **清理**
   - 未入选且无精读的源文 → 删除
   - 保留：入选源文 + `index.json` + `selected.json`

5. **交互指令**：继续 / 详细解释这个句子 / 只讲语法 / 只讲词汇 / 测试我 / 不要翻译

## 精读核心原则

- 以理解意语原文为核心，**不做逐词翻译**。
- A1/A2 级别需更注重**动词变位**标注和**基础语法解释**。
- 词汇分级：A1/A2（基础）→ B1/B2（进阶）→ C1（高级）。
- 重点放在长难句、易误解句、高级词汇、地道/学术表达、论证衔接词。
- 报告要素：原句 / 自然中文 / 句子结构 / 关键词 / 地道表达 / "为什么这样写"；长难句专项。
- 交互指令：继续 / 详细解释这个句子 / 只讲语法 / 只讲词汇 / 测试我 / 不要翻译。

## 注意事项

- 本目录是**独立个人资产**。
- 加新来源：新建 `<source>/` 文件夹，写对应 `fetch_<source>.py`。
- `scan.py` 的 flags 字典需随来源扩充更新。
- **git**：暂不建，预留 `.gitignore`。
- **Quartz 网页部署**：预留 `site/` 目录，未来参照 EnglishRead 的 `site/quartz.config.yaml`。
- **Obsidian**：用户自行配置 `.obsidian/`。
