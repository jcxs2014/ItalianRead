# ItalianRead — 意大利语精读库

中文母语者用高品质意大利语来源做**逐句意语精读**的个人知识库。
目标：从「看中文翻译」过渡到「直接读懂意大利语原文」。

## 目录结构

```
~/Documents/Works/ItalianRead/
├── README.md              ← 本文件
├── AGENTS.md             ← agent 执行规则（入 git，所有 IDE 共享）
├── COLLABORATION.md      ← 协作记录（跨机消息板）
├── .memory/              ← 工作记忆（三层结构，入 git）
│   ├── AGENTS.md           ← 协作基础设施（跨 IDE 共享记忆，入 git）
│   └── daily/              ← 每日工作日志（YYYY-MM-DD.md，入 git）
│   ├── 2026-08-25.md
│   └── 2026-08-26.md
├── .obsidian/            ← Obsidian 配置（用户自行管理，不入git）
├── .gitignore            ← gitignore（含 Quartz + CF Pages）
├── build.sh              ← CF Pages 构建脚本
├── serve.sh              ← 本地预览脚本
├── wrangler.jsonc        ← Workers 配置文件
├── site/                 ← Quartz 静态博客（CF Pages 部署）
│   ├── content/          ← 精读文档源
│   │   ├── index.md      ← 首页
│   │   ├── doppiozero/       ← 文学/文化（B2-C1）
│   │   ├── ilpost/           ← 新闻（B1-B2）
│   │   ├── contropiano/      ← 政治/社会（B2-C1）
│   │   ├── internazionale/   ← 国际新闻（B2-C1）
│   │   ├── treccani/         ← 思源来源（B2-C1）
│   │   ├── lespresso/        ← 思源来源（B1-C1）
│   │   ├── wired/            ← 思源来源（B1-C1）
│   │   └── racconti/         ← 短篇故事精读
│   │       ├── first_italian_reader/      ← 55篇 A2-B1
│   │       ├── italian_short_stories_100/  ← 97篇 A1-A2
│   │       ├── first_italian_readings/     ← 15篇 A2-B1
│   │       ├── italian_reader_en_it/       ← 13篇 A2-B1
│   │       ├── olly_richards/              ← 8篇 A1-A2
│   │       ├── penguin_parallel/           ← 7篇 B1-B2
│   │       └── touri/                      ← 10篇 A1-A2
│   ├── quartz/           ← Quartz 源码树（CLI 壳 + 管线）
│   ├── quartz.config.yaml← Quartz 配置
│   ├── components/        ← 自定义组件（如 Head.tsx PWA 注入）
│   ├── styles/custom.scss← 自定义样式
│   └── public/           ← 构建产物（CF Pages 托管，gitignore）
├── storybook/            ← epub 源文件（不入git）
└── news/                 ← Calibre 新闻抓取（不入git）
    └── scraped/          ← 手动下载的原始文章（不入git）
```

## 内容统计

| 来源                  | 篇数 | 难度     |
| --------------------- | ---- | -------- |
| doppiozero            | 4    | B2-C1   |
| ilpost                | 8    | B1-B2   |
| contropiano           | 7    | B2-C1   |
| internazionale        | 4    | B2-C1   |
| treccani              | 10   | B2-C1   |
| lespresso             | 9    | B1-C1   |
| wired                 | 6    | B1-C1   |
| racconti（故事合计） | 205  | A1-C1   |
| **总计**                | **253** |          |

### racconti 子来源明细（205 篇）

| 来源                  | 篇数 | 难度    | 文件名格式      |
| --------------------- | ---- | ------- | --------------- |
| first_italian_reader  | 55   | A2-B1   | `01_novellino...md` |
| italian_short_stories_100 | 97   | A1-A2   | `001_chef...md` |
| first_italian_readings | 15   | A2-B1   | `01_il_gatto...md` |
| italian_reader_en_it   | 13   | A2-B1   | `01_fortuna...md` |
| olly_richards         | 8    | A1-A2   | `01_la_pizza...md` |
| penguin_parallel      | 7    | B1-B2   | `01_il_lungo...md` |
| touri                 | 10   | A1-A2   | `01_il_ghiacciolo.md` |

## Quartz 部署

### 本地预览

```bash
./serve.sh          # 启动 http://localhost:8080
./serve.sh build    # 仅构建到 site/public/
./serve.sh clean    # 清理产物
```

### Cloudflare Pages 部署

| 参数                  | 值                  |
| --------------------- | ------------------- |
| Build command         | `bash build.sh`    |
| Build output directory| `site/public`        |
| 环境变量              | `NODE_VERSION=22`    |
| 仓库根 `.nvmrc`       | `22`                 |

### 字体（`quartz.config.yaml`）

- 字体加载：header/body 通过 `fontOrigin: googleFonts`
- 视觉字形：Latin Lora + 中文（思源宋 SC）+ 代码 IBM Plex Mono
- ⚠️ **大陆网络**：fonts.googleapis.com 不可达，全站回退 system-ui

### 排序规则（重要）

- `racconti/` 下所有带编号的文档必须在 frontmatter 添加 `modified: <项目启动日>` 字段
- 同目录所有文件 modified 相同 → 稳定排序触发 → 文件名序 01→N 正序
- 详见 `.memory/AGENTS.md`「排序规则」章节

## 记忆与协作分工

| 层 | 文件 | 内容 | 入 git | 变动频率 |
|----|------|------|--------|----------|
| 项目级执行规则 | `AGENTS.md` | 精读流程、命名/日期规范、精读格式、news 工作流、git/推送策略、Quartz 配置红线（排序/字体/前端定制）、交互指令 | ✅ 是 | 低（执行规则变更） |
| 协作基础设施 | `.memory/AGENTS.md` | 跨 IDE 协作约定、记忆系统三层分工说明、Quartz 站点活链结构、目录结构、系统设计决策 | ✅ 是 | 低（协作拓扑变更） |
| 当日工作日志 | `.memory/daily/YYYY-MM-DD.md` | 当日工作日志、调试过程、决策 | ✅ 是 | 高（追加不覆盖） |
| 跨机消息板 | `COLLABORATION.md` | 重要状态/决策/事件 | ✅ 是 | 事件触发 |

**两套 AGENTS.md 分工**：根负责「执行规则」（agent 接到精读任务时必读），.memory 负责「协作基础设施」（多 IDE 间的机器对照与记忆说明）。

## 精读核心原则

- **文章精读**（6 章）：概览 → 逐句精读 → 词汇分级 → 长难句专项 → 精读总结 → 可迁移表达
- **词汇分级四档**：⭐基础(A1-A2) / ⭐⭐中级(B1) / ⭐⭐⭐进阶(B2) / ⭐⭐⭐⭐高级(C1)
- **故事精读**（8 章）：概要 / 原文与解析 / 词汇表 / 固定表达 / 文化注释 / 文学手法 / 主题探讨 / 精读笔记
- **新闻精读**：800-1000 词核心段落 + 完整精读结构

## 来源

| 来源            | 类型        | 难度   |
| --------------- | ----------- | ------ |
| doppiozero      | 文学/文化    | B2-C1  |
| Il Post         | 新闻        | B1-B2  |
| Contropiano     | 政治/社会    | B2-C1  |
| Internazionale  | 国际新闻    | B2-C1  |
| Treccani        | 杂志/文化（思源来源） | B2-C1 |
| L'espresso      | 杂志（思源来源） | B1-C1 |
| Wired Italia    | 科技（思源来源） | B1-C1 |

抓取方式：
- **doppiozero**：唯一有全文的 RSS，自动抓取（`scripts/fetch_doppiozero.py`）
- **Il Post / Internazionale / Contropiano**：Calibre 内置新闻源手动抓取
- **Treccani / L'espresso / Wired**：思源笔记导出 + 整理