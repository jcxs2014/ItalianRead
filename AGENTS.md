# Rule: ItalianRead 精读会话工作流

> **根 AGENTS.md = 执行规则**（入 git，所有 IDE 共享）。Agent 接到精读任务时必读。
> 跨 IDE 协作/记忆分工 → 见 `.memory/AGENTS.md`

## 工作区信息

- **本工作区**：`~/Documents/Works/ItalianRead/`
- **精读保存根目录**：本工作区自身（所有 md 文件保存于此）
- **重要目录**：
  - `storybook/` — 故事 epub 源文件（不 git 追踪）
  - `news/` — 新闻 epub 源文件（不 git 追踪，Calibre 抓取）
  - `site/content/racconti/` — 故事精读文档
  - `site/content/doppiozero/` 等 — 文章精读文档

## 来源清单

### RSS 自动抓取

| 来源       | 难度     | 抓取方式              |
| ---------- | -------- | --------------------- |
| doppiozero | B2-C1    | `scripts/fetch_doppiozero.py`（唯一有全文的 RSS） |

### Calibre 手动抓取（13 个内置意大利语新闻源）

- Il Post, Internazionale, Contropiano, Il Corriere della Sera, Il Fatto Quotidiano,
  Il Manifesto, Il Messaggero, Il Sole 24 Ore, La Repubblica, La Stampa, La Voce, Vitalia, Adnkronos

### 思源笔记来源（手动导出后精读）

| 来源       | 难度     | 路径                              |
| ---------- | -------- | --------------------------------- |
| Treccani   | B2-C1    | `/意语学习/News and Papers/Treccani` |
| L'espresso | B1-C1    | `/意语学习/News and Papers/L'espresso` |
| Wired      | B1-C1    | `/意语学习/News and Papers/Wired`    |

## 精读会话流程

1. 每次收到意大利语文本后，**只在会话中输出简短的状态/标题/简短结构说明**，不输出大段精读内容
2. **完整的精读详情（词汇、语法、写作技巧、句型分析等）直接写入 md 文件**
3. 文件命名格式：
   - **文章**：`标题_snake_case.md`
   - **故事**：`编号_标题_snake_case.md`（编号位数按来源总篇数：<100 篇用 2 位如 `01`，≥100 篇用 3 位如 `001`）
4. 保存路径：
   - **文章**：`site/content/<source>/<日期_星期>/`
   - **故事**：`site/content/racconti/<source>/`
5. 文件名基于标题自动生成（用下划线代替空格，去掉标点）
6. 每次会话开头不再需要等「继续」指令；用户给文本就分析+保存

## 日期文件夹规范

- 文章精读按日期+星期归档到子目录：`<source>/<YYYY-MM-DD_weekday>/`
- 例：`site/content/ilpost/2026-08-23_sunday/01_title.md`
- 故事精读不需要日期文件夹（直接按编号放在 `<source>/` 下）

## 精读格式

### 文章精读（A1-C1）

#### A1/A2 级别精读重点

**针对初级（A1/A2）学习者的特殊处理**

**动词变位标注**

每个原句分析必须包含**动词变位解析**：
- 标注主语人称 + 动词形式
- 解释变位规律（-are/-ere/-ire 三大变位法）
- 指出不规则变位

**名词单复数**

- 标注名词单复数形式
- 解释名词性数配合规则

**前置词搭配**

- 标注动词+前置词、名词+前置词的固定搭配
- 解释常见前置词（a, di, da, per, con, su, in, tra/fra）的用法

**语法解释深度**

- A1/A2 文章：增加**基础语法解释**子项

#### 文件格式

```
# 标题（精读分析）

## 概览
## 逐句精读
## 词汇分级（A1-A2 → C1 四档）
## 长难句专项
## 精读结束总结
## 可迁移表达
```

- 每句原文一个独立分析块（含中文理解/句子结构/动词变位/关键词/表达方式/为什么这样写六子项；A1/A2 增基础语法）
- 原句编号全文连续不重置

### 故事精读（B1-C1）

#### 文件格式

```
# 标题

## 概要（情节摘要+时间地点+主要人物）
## 原文与解析（chunk-by-chunk：原文→翻译→注释）
## 词汇表（精选高频词，重音标注）
## 固定表达（idiomi、proverbi、sette espressioni）
## 文化注释
## 文学手法（叙事视角/意象/语言特点）
## 主题探讨
## 精读笔记（可迁移表达/难句回顾/思考问题）
```

#### 核心原则

- **原文分段呈现**：故事全文分段，每段配翻译和注释
- **词汇从原文中来**：每个词汇注释都指向故事中的具体句子
- **动词变位重点标注**：仅针对对话中的关键句和复杂描写句
- **chunk 结构**：原文→翻译→注释（词汇/语法/手法三选二）

## 会话交互指令

- "继续" = 接着分析下一部分
- "详细解释这个句子" = 只深挖该句
- "只讲语法"/"只讲词汇" = 只分析该维度
- "测试我" = 设计练习不直接给答案
- "不要翻译" = 全意语用简单意语解释意语
- "标难度" = 标注文中各句难度等级

**核心原则**：会话保持精简，详情写入文件。用户读文件而不是会话。

## 新闻精读工作流

### 源文件管理

- `news/` 存放 Calibre 抓取的 epub 新闻（不 git 追踪）
- `news/scraped/` 存放手动下载的原始文章（不 git 追踪）

### 抓取工具

1. **Calibre Fetch News**：用户手动抓取 epub 到 `news/`，用 `ebook-convert` 提取
2. **fetch_doppiozero.py**：doppiozero RSS（唯一有全文的 RSS 源）

### 处理流程

1. 用户用 Calibre 抓取新闻 → epub 保存到 `news/`
2. 用 ebook-convert 提取文本：`ebook-convert "news/xxx.epub" /tmp/xxx.txt`
3. 从文本中选择适合精读的文章（800-1000词核心段落，B1-C1难度）
4. 生成精读文档 → 保存到 `content/<source>/<日期_星期>/`

### 文章选择标准

- 词数：800-1000词（核心段落）
- 难度：B1-C1
- 主题：文化、社会、生活、科技（避免纯政治/体育）
- 语言：清晰规范，有学习价值

## git 与推送策略

| 类型                                          | 处理                                |
| --------------------------------------------- | ----------------------------------- |
| 项目配置（README/AGENTS/COLLABORATION/build.sh/gitignore） | **commit only，不推送**             |
| 精读文档（site/content/）                       | commit + **等用户明确指令再推送**    |
| 网站配置（site/quartz.config.yaml 等）         | commit + **等用户明确指令推送**      |
| 独立子仓库（如 md2web/）                        | 本地 commit，不推送（无远程）        |

## Quartz 配置红线

### 排序规则（racconti/ 必须遵守）

- **racconti/ 下所有带编号的文档必须添加 `modified: <项目启动日>` 字段**（RFC2822 格式，如 `Fri, 22 Aug 2026 00:00:00 +0000`）
- 同目录所有文件 modified 相同 → 触发稳定排序 → 输入序 = 文件名序 = 01→N 正序
- 日期推断：`git log --diff-filter=A -- <目录首篇文件>` 取首篇精读 commit 日期；不确定时统一用 2026-08-22
- `created-modified-date` 插件只读 `created/modified/published`，**不读 `date:`**——旧文档的 `date:` 字段对排序无效

### typography 规则

- `quartz.config.yaml` typography 三个 family 各填**单一名字**（勿用逗号栈，避免 css2 400）
- `custom.scss` 只改 CSS 变量层（`--headerFont/--bodyFont/--codeFont`），禁止在 article/h1 等元素上硬编码 `font-family !important`
- 中西混排：Latin 在前、CJK 在后（如 `"Lora", "Noto Serif SC", serif`）

### 前端定制哲学

- **少而精**：避免堆砌自定义插件和大量 CSS 覆盖
- **升级友好**：定制越少，升级 Quartz 时冲突越少
- **必查项**：每次改完配置必须本地构建验证 + 提交推送才能在 CF 生效

### 红线文件（勿删）

- `site/quartz/worker.ts`（`parse.ts:56` 转译链硬编码引用，删除即构建失败）
- `site/quartz/cli/` + `bootstrap-cli.mjs` + `build.ts`（CLI 壳 + 管线，活链）

### 嵌套副本陷阱

- `site/quartz/` 内严禁出现嵌套副本（如 `site/quartz/quartz/`）
- 唯一合法结构：`site/` 为项目根，`site/quartz/` 为源码树，`site/quartz.config.yaml` 为配置

### PWA 资源

- 必配：manifest.json + 多尺寸 icon (192/512) + apple-touch-icon (180) + theme-color
- 修改后必须 commit + push 才能在 CF 构建产物中生效