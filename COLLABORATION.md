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

### [系统初始化] → All
多 IDE 协作系统已部署
**排序规则**：消息按**最新到最旧**排列（ newest first，顶部是最新的协作记录）

### [2026-08-22 09:20 UTC] [ItalianRead-IDE] → All
**ItalianRead 精读系统初始化**
- **背景**：用户在 ItalianRead 目录下建立意大利语精读工作流
- **来源**：doppiozero（文学/B2-C1）、La Stampa（新闻/B1-B2）、Le Scienze（科学/B1-B2）
- **变更**：创建 AGENTS.md（含 A1/A2 精读规则）、精读文件格式定义、RSS 抓取脚本 ×3
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
| （示例）查看消息板 | [Opencode-IDE] | 🔄 进行中 | 2026-06-22 |

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
