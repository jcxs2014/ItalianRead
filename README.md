# ItalianRead — 意大利语精读库

中文母语者用高品质意大利语来源做**逐句意语精读**的个人知识库。
目标是"从看中文翻译过渡到直接读懂意大利语原文"。

## 目录结构

```
~/Documents/Works/ItalianRead/
├── README.md              ← 本文件（唯一权威项目文档）
├── AGENTS.md             ← agent 操作手册
├── COLLABORATION.md      ← 协作消息板
├── .memory/              ← 本机工作记忆
│   └── ItalianRead_MEMORY.md
├── .gitignore            ← gitignore（含 Quartz + CF Pages）
├── scripts/              ← 抓取脚本
│   ├── fetch_doppiozero.py
│   ├── fetch_lastampa.py
│   ├── fetch_lescienze.py
│   ├── fetch_corriere.py
│   └── fetch_ilsole24ore.py
├── content/              ← Quartz 内容目录（Markdown）
│   ├── index.md          ← 首页
│   ├── doppiozero/       ← 文学/文化（B2-C1）
│   │   └── 20260822_saturday/
│   │       └── *.md      ← 精读文档
│   └── racconti/         ← 短篇故事精读（未来）
│       └── <author>/
├── storybook/            ← epub 源文件目录（不入git）
└── quartz/               ← Quartz 静态博客
    ├── quartz.config.yaml ← Quartz 配置
    ├── package.json       ← Node.js 依赖
    └── public/           ← Quartz 输出（CF Pages 部署）
```

## 来源

| 来源       | RSS URL                                              | 类别   | 难度  |
| ---------- | ---------------------------------------------------- | ------ | ------ |
| doppiozero | `doppiozero.com/articoli-doppiozero/rss.xml`     | 文学/文化 | B2-C1 |

> **注意**：La Stampa / Corriere / Il Sole 24 / Le Scienze 的 RSS 仅含摘要（数十词），不适合精读。如需更多来源，请手动抓取全文或寻找其他 RSS 含全文的来源。

## 每日工作流

> **节奏**：手动触发，用户说"抓文" → 抓文 + 自动选 3-4 篇 + 开精读。

1. **抓文**（手动触发）
   ```bash
   cd ~/Documents/Works/ItalianRead
   python3 scripts/fetch_doppiozero.py
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
   - **合并规则**：每篇原文 + 对应精读合并为一个 `.md` 文件，精读内容优先展示

4. **本地预览**
   ```bash
   ./serve.sh
   ```

5. **交互指令**：继续 / 详细解释这个句子 / 只讲语法 / 只讲词汇 / 测试我 / 不要翻译

## 精读核心原则

- 以理解意语原文为核心，**不做逐词翻译**。
- A1/A2 级别需更注重**动词变位**标注和**基础语法解释**。
- 词汇分级：A1/A2（基础）→ B1/B2（进阶）→ C1（高级）。
- 重点放在长难句、易误解句、高级词汇、地道/学术表达、论证衔接词。
- 报告要素：原句 / 自然中文 / 句子结构 / 关键词 / 地道表达 / "为什么这样写"；长难句专项。
- 交互指令：继续 / 详细解释这个句子 / 只讲语法 / 只讲词汇 / 测试我 / 不要翻译。

## Quartz 静态博客

### 特点
- Obsidian 兼容（wikilinks、backlinks、transclusions）
- 双向图谱视图
- SPA 路由，快速导航
- 全局搜索
- 响应式设计，暗/亮模式切换

### 部署（Cloudflare Pages）

- **构建命令**：`npx quartz build --directory ../content`
- **输出目录**：`public/`
- **环境变量**：`NODE_VERSION=22`

> 注意：本地 `npm install` 只需首次运行或 `package.json` 变化时执行。CF Pages 会自动安装依赖。

### Quartz 命令

```bash
cd quartz
npm install                              # 首次安装依赖
npx quartz build --directory ../content  # 生产构建
```

## 注意事项

- 加新来源：新建 `content/<source>/` 目录，写对应 `scripts/fetch_<source>.py`
- 短篇故事：`content/racconti/<author>/<index>_slug.md`（三位编号 000-999）
  - epub 源文件放入 `storybook/`（不入git）
  - 提取脚本 TBD
- **Obsidian**：用户自行配置 `.obsidian/`
- **.gitignore**：已配置 Quartz 输出、Python 缓存、macOS 临时文件等
- **合并精读**：同一文章的原文 `.md` 和 `_jindu.md` 需要手动合并（未来可自动化）
