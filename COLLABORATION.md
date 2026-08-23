# Agent 协作消息板

**用途**：同一台机器、同一目录下不同 IDE 实例的 agents 之间留言和协作
**同步方式**：两个 IDE 共享同一份文件系统，**写入本文件后对方即时可见，无需 `git pull/push`**
**读取方式**：直接打开本文件，或运行 `./check_collab.sh`

**🆔 IDE 身份约定**（**纯规则，无配置文件**）：
- **不写入任何文件或环境变量**——每个 IDE/TUI 在对话中**自己声明身份**
- 首次工作时：明确告知，如 "我是 Opencode-IDE"
- 每次写消息/提交：前缀标注 `[IDE名]`，如 `### [时间戳] [Opencode-IDE] → All`
- **命名格式**：`<IDE名>-<机器名>`，统一格式，禁止混用旧写法
  - ✅ 正确：`Opencode-IDE`、`CodeBuddy-Mac`、`ZCode-Mac`
  - ❌ 错误：`CodeBuddy` / `CodeBuddy-CN` / `Opencode`（缺少机器名或格式不一）

**🕐 时区约定**（**所有时间戳用 UTC**）：
- 格式：`YYYY-MM-DD HH:MM UTC`
- 查询命令：`date -u '+%Y-%m-%d %H:%M UTC'`
- 理由：跨时区无歧义、国际标准、git 友好

**📁 记忆目录**：
- 新项目使用 `.memory/`（通用、跨 IDE、隐藏目录）
- 兼容旧项目：`.codebuddy/memory/` / `.opencode/` / `.claude/` 等
- 优先级：环境变量 > 命令行 > 项目内已存在目录

---

## 📨 消息列表

### [2026-08-23 16:30 UTC] [ItalianRead-IDE] → All
**first_italian_reader 精读内容全部完成（55篇）**

- **背景**：epub XML重新提取后，55篇全部生成完整精读结构
- **变更**：55篇全部含原文段落+翻译+注释框架，词汇表/固定表达/文化注释/文学手法/主题探讨/精读笔记各章节完整
- **Commit**: `93e9985`

### [2026-08-23 14:30 UTC] [ItalianRead-IDE] → All
**first_italian_reader 精读重新生成完成（55篇）**

- **背景**：发现 Calibre txt 提取导致意英内容交错混合，改用 epub 原始 XML 提取
- **变更**：
  - 新增 `scripts/re_extract_first_italian_reader.py`（epub XML 提取）
  - `storybook/first_italian_reader/` 55篇源文件重新提取（849→完整）
  - 精读文件全部重新生成（110 files changed, commit `ce5b4e5`）
- **质量**：Novellino 确认含完整3篇novelle（含狐狸寓言C段）

### [2026-08-23 12:55 UTC] [ItalianRead-IDE] → All
**脚本清理 + .nvmrc 移至根目录**

- 删除 fetch_ilpost.py、fetch_trafilatura.py（测试无效）
- .nvmrc 从 site/ 移到根目录（CF 构建机生效）
- news/scraped/ 目录创建（手动下载文章存放）
- Commit: `7c131ba`

### [2026-08-23 12:30 UTC] [ItalianRead-IDE] → All
**CF Pages 部署完成 + 重构收尾**

- **背景**：将 Quartz 结构对齐 EnglishRead（site/ 根目录），解决 build.sh 路径 bug
- **变更**：
  - Quartz 从 `quartz/` 上提到 `site/quartz/`（package.json/tsconfig.json/quartz.config.yaml 等移至 site/ 根）
  - `build.sh` 修正：`cd site && npx quartz build -d content`
  - `wrangler.jsonc`：`assets.directory` → `./site/public`
  - `.gitignore` 清理：移除死规则、添加 `site/quartz/node_modules/`、`setup_obsidian.sh`
  - 软连接不入库：`check_collab.sh`/`setup_multi_ide.sh`/`sync_memory.sh` 移除追踪
  - doppiozero 日期目录统一：`20260822_saturday` → `2026-08-22_saturday`
- **Commit**: `01f5d1c` / `2a0e52f`
- **状态**: ✅ 推送完成，等待 CF 构建确认

### [2026-08-23 11:50 UTC] [ItalianRead-IDE] → All
**CF Pages 推送就绪**

- GitHub: `git@github.com:jcxs2014/ItalianRead.git`
- 本地验证：229 markdown → 282 HTML，零报错
- baseUrl: `italianread.jcxs2014.workers.dev`
- CF 构建命令：`bash build.sh`
- CF 输出目录：`site/public`
- 环境变量：`NODE_VERSION=22`

### [2026-08-22 22:00 UTC] [ItalianRead-IDE] → All
**新闻精读完成：Il Post 8篇 + Contropiano 7篇 + Internazionale 4篇 = 19篇**

- **核心段落方案**：800-1000词 + 完整精读结构
- **Commit**: `eef1d74` (Il Post) → `cd9b4dc` (Contropiano) → `12863d3` (Internazionale 重做)
- **新闻精读总计**: 19篇
- **精读总进度**: 228篇（209故事 + 19新闻）

### [2026-08-22 14:00 UTC] [ItalianRead-IDE] → All
**storybook 清理完成 + 全部精读收尾**
- **背景**：对比 storybook（原始提取）与 content/racconti（精读）差异，清理不适合精读的来源
- **变更**：
  - 删除 8 个不适合目录：learn_like_native（提取损坏）、penguin_short_stories（英译文）、talk_in_italian（词汇教材）、ultimate_guide（词汇书）、modern_italian_grammar（语法书）、italian_stories_hall（文学史）、easy_italian_reader（语法复习）、vita_nuova（英译文）
  - 新增 first_italian_readings 15篇精读（Perrault/Collodi 童话 + De Amicis + Capuana + Pascoli 等，A2-B1）
  - 验证 touri 10篇已完整（storybook 编号偏移但 racconti 无缺）
  - storybook 保留7个来源，与 content/racconti 完全同步
- **Commit**：`ecd6451`（first_italian_readings）
- **精读总计**：209篇（4篇文章 + 205个故事）
- **状态**：✅ 已完成

### [系统初始化] → All
多 IDE 协作系统已部署
**排序规则**：消息按**最新到最旧**排列（ newest first，顶部是最新的协作记录）

### [2026-08-22 11:10 UTC] [ItalianRead-IDE] → All
**弃用 Hugo，改用 Quartz v5 静态博客**
- **背景**：Hextra 主题不适合精读文档（嵌套结构、词汇表渲染差）；用户决定换回 Quartz
- **变更**：
  - 删除 `site/`（Hugo 全部配置）
  - 克隆 Quartz v5 到 `quartz/` 目录
  - 配置 `quartz.config.yaml`：baseUrl="", pageTitle="ItalianRead"
  - 内容目录：`../content/articoli`（通过 `--directory` 参数指定）
  - 合并精读：原文 + 中文精读分析合并为一个 `.md`（精读优先）
  - 本地预览：`cd quartz && npx quartz build --directory ../content/articoli --serve`（port 8080）
  - CF Pages 部署命令：`npx quartz build --directory ../content/articoli`，输出 `public/`
  - 更新 `.gitignore`（Quartz 输出目录）
  - 更新 `README.md`（Quartz 部署说明）
- **待处理**：合并脚本自动化（目前需手动合并 `_jindu.md` 到原文）
- **状态**：✅ 本地测试通过

### [2026-08-22 09:40 UTC] [ItalianRead-IDE] → All
**Hugo 站点修复：语言切换英文 / 排除 src.md / public 不入 git**
- **变更**：
  - locale 改为 `en-US`，菜单改为英文（Articles/Tags/Categories）
  - `.src.md` 重命名为 `.md`，Hugo 正常构建（24 pages）
  - `.gitignore` 已含 `site/public/`（CF Pages 部署不追踪构建产物）
- **状态**：✅ 已完成

### [2026-08-22 09:35 UTC] [ItalianRead-IDE] → All
**Hugo 静态博客初始化完成（Hextra + PaperMod fallback）**
- **背景**：用户决定使用 Hugo + Hextra 做静态博客（替代 Quartz）
- **变更**：
  - 初始化 Hugo 站点（`site/` 目录）
  - 安装 Hugo + Go（Hombrew）
  - 添加 Hextra v0.12.3（主主题）+ PaperMod（fallback）
  - 配置 hugo.toml：响应式/暗亮切换/tag分类/多级目录
  - CF Pages 部署配置
  - 构建测试通过（11 pages）
- **相关文件**：`site/hugo.toml`、`site/themes/`
- **状态**：✅ 已完成
- **注意**：PaperMod submodule 需在干净 clone 后执行 `git submodule update --init --recursive`

### [2026-08-22 09:30 UTC] [ItalianRead-IDE] → All
**重构：采用 Hugo 静态博客方案，调整目录结构**
- **背景**：用户决定使用 Hugo 替代 Quartz 做静态博客部署
- **变更**：
  - 抓取脚本移至 `scripts/`
  - 文章移至 `content/articles/<source>/`
  - 新增 `site/` 预留 Hugo 输出目录
  - 更新 `.gitignore`（Hugo + Cloudflare Pages）
  - 修正所有脚本 `datetime.utcnow()` deprecated 警告
- **相关文件**：`scripts/`、`content/articles/`、`.gitignore`
- **状态**：✅ 已完成

### [2026-08-22 09:25 UTC] [ItalianRead-IDE] → All
**完成首次精读：doppiozero — Portello《凝视的治疗力量》**
- **背景**：测试精读流程；发现repubblica有付费墙，改用doppiozero（有全文）
- **变更**：新增精读文件 `02_mauro_portello_la_terapia_dello_sguardo_jindu.md`（412行）
- **相关文件**：`doppiozero/20260822_saturday/02_mauro_portello_la_terapia_dello_sguardo_jindu.md`
- **状态**：✅ 已完成

### [2026-08-22 09:20 UTC] [ItalianRead-IDE] → All
**ItalianRead 精读系统初始化**
- **背景**：用户在 ItalianRead 目录下建立意大利语精读工作流
- **来源**：doppiozero（文学/B2-C1）、La Stampa（新闻/B1-B2）、Le Scienze（科学/B1-B2）、Corriere della Sera（新闻/B1-B2）、La Repubblica（新闻/B1-B2）、Il Sole 24 Ore（经济/B2）
- **变更**：创建 AGENTS.md（含 A1/A2 精读规则）、精读文件格式定义、RSS 抓取脚本 ×6
- **相关文件**：`AGENTS.md`、`doppiozero/`、`lastampa/`、`lescienze/`
- **状态**：✅ 已完成

**使用格式（结构化）**：
```markdown
### [YYYY-MM-DD HH:MM UTC] [发送者IDE名] → [接收者IDE名 或 All]
**主题**（一句话描述）
- **背景**：问题的起因或任务的动机
- **变更**：具体改动内容（代码/文档/参数）
- **Commit**：git commit hash（如有）
- **相关文件**：涉及的文件路径
- **状态**：✅ 已完成 / 🔄 进行中 / ⏳ 等待中
```

**简化格式**（简单消息）：
```markdown
### [时间戳] [IDE名] → All
消息内容
```

**示例（结构化）**：
```markdown
### [2026-06-22 12:30 UTC] [Opencode-IDE] → All
**IDE 身份声明**
- 身份：[Opencode-IDE]
- 状态：✅ 已加入协作系统
```

**示例（工作记录）**：
```markdown
### [2026-07-10 14:00 UTC] [CodeBuddy-Mac] → All
**完成数据预处理流程**
- **背景**：用户要求自动化批量处理
- **变更**：新增 `preprocess.py`（支持 --batch 参数）；重构 `config.yaml` 结构
- **Commit**：`a1b2c3d`
- **相关文件**：`scripts/preprocess.py`、`config/config.yaml`
- **状态**：✅ 已完成
```

---

## 📊 任务看板

> **排序规则**：按 `最后更新 (UTC)` 倒序排列（最新在前）。新任务统一追加到表顶部。示例行仅作格式参考，正式任务看板应填入真实任务。

| 任务 | 负责人 (IDE) | 状态 | 最后更新 (UTC) |
|------|----------|------|----------|
| 精读系统完成（209篇） | [ItalianRead-IDE] | ✅ 已完成 | 2026-08-22 |
| storybook 清理（8个目录删除） | [ItalianRead-IDE] | ✅ 已完成 | 2026-08-22 |
| CF Pages 部署 | [ItalianRead-IDE] | ⏳ 待处理 | 2026-08-22 |

---

## 📝 协作日志

*（此区域自动生成，记录重要的协作事件）*

---

**维护说明**：
1. 添加消息前，**确认已在对话中声明自己的 IDE 身份**
2. 添加消息后，对方在同目录下即时可见
3. 无需 `git pull`——同目录共享文件系统
4. 任务状态变更时，更新"任务看板"区域
5. 每个 IDE 的协作记录：`git log --all --grep='[IDE名]' --oneline`
6. 定期清理过期消息（见 🧹 消息清理规则）

---

## 🧹 消息清理规则

**建议**：每周清理一次过期消息，避免文件过大。

### 清理示例
```bash
# 1. 创建归档文件
cp COLLABORATION.md COLLABORATION_ARCHIVE_20260622.md

# 2. 编辑 COLLABORATION.md，删除过期消息（保留格式说明行）

# 3. 提交归档
git add COLLABORATION.md COLLABORATION_ARCHIVE_20260622.md
git commit -m "协作消息板：清理过期消息（归档至 COLLABORATION_ARCHIVE_20260622.md）"
```

---

## ❓ 常见问题 (FAQ)

### Q1: 我看不到其他 IDE 的消息？
**A**: 确认：
1. 两个 IDE 在**同一台机器、同一目录**打开此项目
2. 对方已经**保存了 COLLABORATION.md**（不是仅编辑未保存）
3. 刷新文件（在 IDE 中重新打开 COLLABORATION.md）

### Q2: 如何避免消息冲突？
**A**:
- 每个 IDE 在消息中**明确标注自己的身份**（如 `[Opencode-IDE]`）
- 使用 `./check_collab.sh` 查看消息板后再添加新消息
- 任务看板中**明确标注负责人 IDE**

### Q3: 消息格式有误怎么办？
**A**: 直接编辑 COLLABORATION.md 修正格式，无需特殊权限。

### Q4: 如何查找特定 IDE 的所有消息？
**A**:
```bash
# 方法1：在 COLLABORATION.md 中搜索
grep "\[Opencode-IDE\]" COLLABORATION.md

# 方法2：查找 git 提交历史
git log --all --grep="\[Opencode-IDE\]" --oneline
```

### Q5: sync_memory.sh 报错 "not a git repository"？
**A**: 确认当前目录是 Git 仓库：
```bash
git status  # 应该在项目根目录
```

### Q6: 消息时间戳应该用哪个时区？
**A**: **统一使用 UTC**：
- 格式：`2026-06-22 10:30 UTC`
- 查询命令：`date -u '+%Y-%m-%d %H:%M UTC'`
- 理由：跨时区无歧义、国际标准、git 友好

### Q7: 如何换算 UTC 到本地时间？
**A**:
```bash
# UTC → 本地
date -d "2026-06-22 10:30 UTC" '+%Y-%m-%d %H:%M %Z'
# 本地 → UTC
date -u '+%Y-%m-%d %H:%M UTC'
```

### Q8: 记忆目录可以自定义吗？
**A**: 可以，有 3 种方式（按优先级）：
1. 环境变量：`export MEMORY_DIR=.memory`
2. 安装参数：`bash setup_multi_ide.sh --memory-dir .opencode`
3. 已存在目录：自动检测（`.memory/` > `memory/` > `.codebuddy/memory/` > `.opencode/` > `.claude/` > `.cursor/`）

---

## 📞 联系与反馈

遇到协作系统问题，请在"消息列表"中添加消息：
```markdown
### [时间戳] [你的IDE名] → All
**问题**：描述你遇到的问题
**期望**：描述你期望的行为
```
