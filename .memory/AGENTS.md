# ItalianRead 跨 IDE 共享记忆（拓扑 + 协作日志）

> 注意：本文档为跨 IDE 共享记忆，非操作规则；操作规则见根 `AGENTS.md`，项目说明见 `README.md`。

## 是什么
中文母语者的意大利语**逐句精读**知识库。目标：从"看中文翻译"过渡到"直接读懂意大利语原文"。
学习者水平 A1/A2 起步，覆盖至 B2-C1。

## 协作约定（跨 IDE）
- 同一目录多 IDE 共享文件系统，写入即同步，**无需 git pull/push**
- 时间戳一律 **UTC**（`date -u '+%Y-%m-%d %H:%M UTC'`）
- 消息/commit 前缀：`[IDE名-机器名]`（本机身份：`Opencode-MAC`）
- 记忆目录：`.memory/`（本文件为共享记忆宿主）
- 三层分工：**本文件** = 项目级长期记忆 + 协作协议（变动少）；**`.memory/daily/YYYY-MM-DD.md`** = 每日工作日志（高频追加，不覆盖）；**`COLLABORATION.md`** = 跨机消息板（重要状态/决策/事件，简短）
- 来源/工作流/精读规则 → 详见根 `AGENTS.md` / `README.md`

## 目录结构
- `storybook/<source>/` — 故事 epub 源（不 git 追踪）
- `news/` — 新闻 epub 源（不 git 追踪，Calibre 抓取）
- `site/content/` — 精读文档（**真内容在这里**）
- `site/quartz/` — Quartz 源码树（活链：内层 CLI 管线 + 外层配置组件，见下）
- `site/public/` — 构建产物（gitignore）

## 文件命名规范
- **故事**：`编号_标题_snake_case.md`（编号按来源总篇数：<100 用 2 位，≥100 用 3 位）
- **文章**：`标题_snake_case.md`，目录 `<source>/<日期_星期>/`
- frontmatter：`lang: it` / `状态` / `难度` / `source` / `author` / `originalUrl`

## Quartz 站点（关键结构 2026-08-25 实证）
- **构建入口**：`cd site && npx quartz build -d content`（build.sh / serve.sh 统一）
- **活链双树**：CWD=site/ 下 npx quartz 走 bin→`site/quartz/bootstrap-cli.mjs`（内层=CLI 壳 + build.ts 管线 + processors/util）；esbuild `fp="./quartz/build.ts"` 内 `import cfg from "../quartz"` 解析到外层 `site/quartz.ts`；config-loader 读 `process.cwd()/quartz.config.yaml`=外层
- **勿删活文件**：`site/quartz/worker.ts`（parse.ts:56 转译链硬编码引用）
- **已删除死副本**：`site/quartz/quartz/` 嵌套树 + 旧根遗留（commit 09282e3）
- **字体约定**：Latin 一律 Lora 打头、中文回退 Noto Serif SC（宋体）、代码 IBM Plex Mono；config 管加载（单一 family 名防 css2 400），custom.scss 只改变量层禁硬编码
- **PWA**：manifest.json + icon-72~512 + apple-touch-icon + theme-color 已配置（Head.tsx 注入）
- **favicon 插件**：已启用（外层 config）

## 系统设计决策
1. **Git**：已启用，推送需等用户明确指令（精读文档+网站配置推送需逐次确认）
2. **只建议不直接改**：跨项目工作（EnglishRead）只给建议；本工作区精读生成流程不变
3. **抓取**：doppiozero RSS（唯一全文源）；其余新闻源 Calibre 抓取 → `news/`
4. **来源**：racconti 故事已全部精读完成；新文章来源含思源笔记（lespresso/wired/treccani）
5. **Obsidian 用户自配**——`.obsidian/` 由用户自行设置

## 日记忆约定
- 每日事项落到 `.memory/daily/YYYY-MM-DD.md`（追加，不覆盖）；项目级长期记忆落本文件。
- 各机独立维护，不入 git；跨机协调一律走 `COLLABORATION.md`。
- **不使用** `HERMES_MEMORY/` 等其他本地记忆目录——`.memory/` 是本机唯一工作记忆宿主。
- 高频变动的统计数据（精读篇数等）只记到 daily，不写本文件。

## 精读格式要点
- frontmatter 含 `lang: it`
- A1/A2 级别增加动词变位标注、名词单复数、前置词搭配、基础语法解释
- 词汇分级四档：A1-A2 / B1 / B2 / C1
- 原句编号全文连续不重置
- 故事精读 7 章：概要 / 原文与解析 / 词汇表 / 固定表达 / 文化注释 / 文学手法 / 主题探讨 / 精读笔记
- 文章精读：概览 / 逐句精读 / 词汇分级 / 长难句专项 / 精读总结 / 可迁移表达