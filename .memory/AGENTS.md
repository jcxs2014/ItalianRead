# ItalianRead 跨 IDE 共享记忆（拓扑 + 协作日志）

> **.memory/AGENTS.md = 协作基础设施**（入 git，与根 `AGENTS.md` 同步共享）。
> 执行规则见根 `AGENTS.md`；当日工作见 `.memory/daily/YYYY-MM-DD.md`；跨 IDE 消息见 `COLLABORATION.md`。

## 是什么

中文母语者的意大利语**逐句精读**知识库。目标：从"看中文翻译"过渡到"直接读懂意大利语原文"。
学习者水平 A1/A2 起步，覆盖至 B2-C1。

## 协作约定（跨 IDE）

- 同一目录多 IDE 共享文件系统，写入即同步，**无需 git pull/push**
- 时间戳一律 **UTC**（`date -u '+%Y-%m-%d %H:%M UTC'`）
- 消息/commit 前缀：`[IDE名-机器名]`（本机身份：`Opencode-MAC`）
- 记忆目录：`.memory/`（本文件为共享记忆宿主）
- **⚠️ 记忆系统四层分工**：

| 层 | 文件 | 内容 | 变动频率 |
|---|---|---|---|
| 执行规则 | 根 `AGENTS.md` | 精读格式、文件命名、git 策略、交互指令、Quartz 红线 | 低 |
| 共享记忆 | `.memory/AGENTS.md` | 协作约定、机器信息、记忆系统说明 | 低 |
| 当日日志 | `.memory/daily/YYYY-MM-DD.md` | 当日工作日志、调试过程、决策 | 高 |
| 消息板 | `COLLABORATION.md` | 跨机消息、重要状态/决策 | 事件触发 |

## 目录结构

- `storybook/<source>/` — 故事 epub 源（不 git 追踪）
- `news/` — 新闻 epub 源（不 git 追踪，Calibre 抓取）
- `site/content/` — 精读文档（**真内容在这里**）
- `site/quartz/` — Quartz 源码树（活链：内层 CLI 管线 + 外层配置组件）
- `site/public/` — 构建产物（gitignore）

## Quartz 站点（关键结构 2026-08-25 实证）

- **构建入口**：`cd site && npx quartz build -d content`（build.sh / serve.sh 统一）
- **活链双树**：CWD=site/ 下 npx quartz 走 bin→`site/quartz/bootstrap-cli.mjs`（内层=CLI 壳 + build.ts 管线 + processors/util）；esbuild `fp="./quartz/build.ts"` 内 `import cfg from "../quartz"` 解析到外层 `site/quartz.ts`；config-loader 读 `process.cwd()/quartz.config.yaml`=外层
- **勿删活文件**：`site/quartz/worker.ts`（parse.ts:56 转译链硬编码引用）
- **已删除死副本**：`site/quartz/quartz/` 嵌套树 + 旧根遗留（commit 09282e3）

## 系统设计决策

1. **Git**：已启用，推送需等用户明确指令（精读文档+网站配置推送需逐次确认）
2. **只建议不直接改**：跨项目工作（EnglishRead）只给建议；本工作区精读生成流程不变
3. **抓取**：doppiozero RSS（唯一全文源）；其余新闻源 Calibre 抓取 → `news/`
4. **来源**：racconti 故事已全部精读完成；新文章来源含思源笔记（lespresso/wired/treccani）
5. **Obsidian 用户自配**——`.obsidian/` 由用户自行设置

## 日记忆约定

- 每日事项落到 `.memory/daily/YYYY-MM-DD.md`（追加，不覆盖）；项目级长期记忆落根 `AGENTS.md` 或本文件
- 各机通过 git 同步；跨机协调走 `COLLABORATION.md` + git
- **不使用** `HERMES_MEMORY/` 等其他本地记忆目录——`.memory/` 是本机唯一工作记忆宿主
- 高频变动的统计数据（精读篇数等）只记到 daily，不写本文件
- 两个 AGENTS.md 分工：根 `AGENTS.md` = 执行规则（入 git）；`.memory/AGENTS.md` = 协作基础设施（入 git）