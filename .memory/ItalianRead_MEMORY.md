# ItalianRead 项目记忆

## 基本信息
- **工作区**：`~/Documents/Works/ItalianRead/`
- **初始化日期**：2026-08-22
- **语言**：意大利语精读
- **学习者水平**：A1/A2 起步，覆盖至 B2-C1

## 精读库现状（2026-08-25 共 253 篇）
| 来源 | 篇数 | 说明 |
| ---- | ---- | ---- |
| racconti（故事） | 205 | 7 个子来源（first_italian_reader 55 / italian_short_stories 97 / first_italian_readings 15 / italian_reader_en_it 13 / olly_richards 8 / penguin_parallel 7 / touri 10） |
| ilpost | 8 | 新闻 B1-B2 |
| treccani | 10 | 文章 B2-C1 |
| lespresso | 9 | 文章 B1-C1（来源：思源笔记） |
| contropiano | 7 | 新闻 B2-C1 |
| wired | 6 | 文章 B1-C1（来源：思源笔记） |
| doppiozero | 4 | 文章 B2-C1 |

## 目录结构
- `storybook/<source>/` — 故事 epub 源（不 git 追踪）
- `news/` — 新闻 epub 源（不 git 追踪）
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
4. **来源**：racconti 故事已全部精读完成；新文章来源含思源笔记（lespresso/wired）
5. **Obsidian 用户自配**——`.obsidian/` 由用户自行设置

## 精读格式要点
- frontmatter 含 `lang: it`
- A1/A2 级别增加动词变位标注、名词单复数、前置词搭配、基础语法解释
- 词汇分级四档：A1-A2 / B1 / B2 / C1
- 原句编号全文连续不重置
- 故事精读 7 章：概要 / 原文与解析 / 词汇表 / 固定表达 / 文化注释 / 文学手法 / 主题探讨 / 精读笔记
- 文章精读：概览 / 逐句精读 / 词汇分级 / 长难句专项 / 精读总结 / 可迁移表达