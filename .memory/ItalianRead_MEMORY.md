# ItalianRead 项目记忆

## 基本信息
- **工作区**：`~/Documents/Works/ItalianRead/`
- **初始化日期**：2026-08-22
- **语言**：意大利语精读
- **学习者水平**：A1/A2 起步，可进阶到 B 级

## 来源配置

| 来源 | 文件夹 | RSS URL | 难度 |
| ---- | ------ | ------- | ---- |
| doppiozero | doppiozero/ | doppiozero.com/articoli-doppiozero/rss.xml | B2-C1 |
| La Stampa | lastampa/ | lastampa.it/rss | B1-B2 |
| Le Scienze | lescienze/ | lescienze.it/rss | B1-B2 |

## 文件命名规范
- 原文：`标题_snake_case.src.md`
- 精读：`标题_snake_case_精读.md`
- 目录：`<source>/<日期_星期>/`

## 系统设计决策
1. **暂不建 git**——预留 `.gitignore`
2. **手动触发抓取**——用户说"抓文"才执行
3. **每源每次选 3-4 篇**
4. **去重机制**——检查之前已抓取的 URL
5. **Quartz 预留**——`site/quartz.config.yaml` 未来配置
6. **Obsidian 用户自配**——`.obsidian/` 由用户自行设置

## 精读格式要点
- frontmatter 含 `lang: it`
- A1/A2 级别增加动词变位标注和基础语法解释
- 词汇分级四档：A1-A2 / B1 / B2 / C1
- 原句编号全文连续不重置
