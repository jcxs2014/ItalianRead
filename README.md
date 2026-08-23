# ItalianRead — 意大利语精读库

中文母语者用高品质意大利语来源做**逐句意语精读**的个人知识库。
目标是"从看中文翻译过渡到直接读懂意大利语原文"。

## 目录结构

```
~/Documents/Works/ItalianRead/
├── README.md              ← 本文件
├── AGENTS.md             ← agent 操作手册
├── COLLABORATION.md      ← 协作记录
├── .memory/              ← 本机工作记忆
├── .obsidian/            ← Obsidian 配置（用户自行管理，不入git）
├── .gitignore            ← gitignore（含 Quartz + CF Pages）
├── build.sh              ← CF Pages 构建脚本
├── serve.sh              ← 本地预览脚本
├── wrangler.jsonc        ← Workers 配置文件
├── scripts/              ← 抓取脚本
│   ├── fetch_doppiozero.py
│   └── ...
├── site/                 ← Quartz 静态博客（CF Pages 部署）
│   ├── content/          ← 精读文档源
│   │   ├── index.md      ← 首页
│   │   ├── doppiozero/   ← 文学/文化（B2-C1）
│   │   ├── ilpost/       ← 新闻（B1-B2）
│   │   ├── contropiano/  ← 新闻（B2-C1）
│   │   ├── internazionale/ ← 国际新闻（B2-C1）
│   │   └── racconti/     ← 短篇故事精读
│   │       ├── first_italian_reader/    ← 55篇
│   │       ├── italian_short_stories_100/ ← 97篇
│   │       ├── penguin_parallel/         ← 7篇
│   │       └── ...
│   ├── quartz/           ← Quartz 框架
│   │   ├── quartz.config.yaml
│   │   ├── package.json
│   │   └── public/       ← 构建产物（自动生成）
│   └── public/           ← 静态输出（CF Pages 托管）
├── storybook/            ← epub 源文件（不入git）
└── news/                 ← Calibre 新闻抓取（不入git）
```

## 内容统计

| 来源                      | 篇数 | 难度     |
| ------------------------- | ---- | -------- |
| doppiozero                | 4    | B2-C1   |
| ilpost                    | 8    | B1-B2   |
| contropiano               | 7    | B2-C1   |
| internazionale            | 4    | B2-C1   |
| racconti (总计)           | 205  | A2-C1   |
| **总计**                      | **228** |          |

## Quartz 部署

### 本地预览

```bash
./serve.sh          # 启动 http://localhost:8080
./serve.sh build    # 仅构建
./serve.sh clean    # 清理产物
```

### Cloudflare Pages 部署

- **Build command**: `bash build.sh`
- **Build output directory**: `site/public`
- **环境变量**: `NODE_VERSION=22`

### Quartz 命令

```bash
cd site
npm install --legacy-peer-deps
npx quartz build -d content    # 构建
```

## 精读核心原则

- **精读格式**：概览 → 逐句精读（中文理解/句子结构/动词变位/关键词/表达方式）→ 词汇分级 → 长难句 → 总结 → 可迁移表达
- **词汇分级**：⭐基础(A1-A2) / ⭐⭐中级(B1) / ⭐⭐⭐进阶(B2) / ⭐⭐⭐⭐高级(C1)
- **故事精读**：chunk分段结构（原文→翻译→注释）+ 词汇表 + 固定表达 + 文化注释 + 文学手法 + 主题探讨 + 精读笔记
- **新闻精读**：800-1000词核心段落 + 完整精读结构

## 来源

| 来源           | 类型   | 难度  |
| -------------- | ------ | ----- |
| doppiozero     | 文学/文化 | B2-C1 |
| Il Post        | 新闻   | B1-B2 |
| Contropiano    | 政治/社会 | B2-C1 |
| Internazionale  | 国际   | B2-C1 |

Calibre 新闻源（需手动抓取）：Il Post, Internazionale, Contropiano 等。
