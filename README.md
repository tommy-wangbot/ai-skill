# ai-skill

> 🧠 跨平台 AI Skills 统一仓库 | by [@tommy-wangbot](https://github.com/tommy-wangbot)

GitHub 仓库 = 唯一 source of truth。
公共 skill 内容放在 `skills/`，平台专属配置放在 `overlays/`，
由 `scripts/sync-skills.sh` 合并生成到各平台的运行时目录。

---

## 仓库结构

```
ai-skill/
├── skills/                  # 公共 Skill 内容（平台无关）
│   ├── commit/SKILL.md
│   └── ...
├── overlays/                # 平台专属补丁（同名文件覆盖公共内容）
│   ├── codex/               # agents/openai.yaml
│   └── hermes/              # hermes 专属配置
├── dist/                    # ⚠️ 生成产物，已 gitignore，勿手动编辑
├── scripts/
│   └── sync-skills.sh       # 合并 + 分发脚本
└── README.md
```

---

## 快速开始

```bash
# 1. clone 仓库
git clone https://github.com/tommy-wangbot/ai-skill.git ~/ai-skill
cd ~/ai-skill

# 2. 一键同步到所有平台
./scripts/sync-skills.sh

# 3. 只同步某个平台
./scripts/sync-skills.sh claude
./scripts/sync-skills.sh codex
./scripts/sync-skills.sh hermes
```

| 平台 | 运行时目录 |
|------|-----------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Hermes | `~/.hermes/skills/` |

---

## Skills 目录（共 72 个）

### 一类：通用型 · 推荐全平台安装（21个）

| Skill | 功能描述 |
|-------|---------|
| `commit` | Conventional Commits 规范提交信息生成 |
| `epic` | 创建和管理 Epic 大型功能集合 |
| `issue` | 创建和管理本地 Issue 任务规格 |
| `publish` | 通过 GitHub Actions 发布新版本 |
| `plan-mode` | 进入结构化规划模式，输出多步方案 |
| `todo` | 基于 Markdown 文件的任务清单管理 |
| `tasks` | 跨会话的多步骤全局任务追踪 |
| `memory-management` | 搜索和管理历史对话记忆 |
| `web-search` | 联网搜索最新信息 |
| `web-fetch` | 抓取和读取网页内容 |
| `find-skills` | 智能发现和推荐可安装的 Skills |
| `multi-search-engine` | 17 个搜索引擎，无需 API Key |
| `self-improving-agent` | 持续捕获错误和改进经验 |
| `prompt-optimizer` | 将模糊 Prompt 优化为稳定可靠的指令 |
| `gstack-office-hours` | YC Office Hours 模式：创业逼问 / Builder 头脑风暴 |
| `gstack-retro` | 周度工程复盘：commit 分析、工作模式、代码质量趋势 |
| `brainstorming` | 创意发散：功能设计前强制探索用户意图与需求 |
| `dispatching-parallel-agents` | 多 Agent 并行调度，处理相互独立的子任务 |
| `using-superpowers` | 对话启动时自动发现和调用可用 Skills |
| `fireworks-tech-graph` | 生成生产级 SVG+PNG 技术图表，14种图类 + 7种视觉风格 |
| `diagram-generator` | 多格式图表生成：Draw.io / Mermaid / Excalidraw（需 MCP）|

### 二类：内容处理型 · 按需安装（17个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `baoyu-translate` | Codex | 三模式翻译：快速 / 普通 / 精翻 |
| `tech-translation-expert` | Codex | 宝玉风格技术文章中英互译 |
| `baoyu-format-markdown` | Codex | Markdown 格式化与美化 |
| `baoyu-url-to-markdown` | Codex | 网页转 Markdown（支持需登录页面）|
| `baoyu-danger-x-to-markdown` | Codex | X/Twitter 推文转 Markdown |
| `baoyu-youtube-transcript` | 社区 | YouTube 字幕提取，多语言 + 章节 + 说话人识别 |
| `wechat-to-markdown` | Codex | 微信公众号文章转 Markdown + 图片下载 |
| `jina-cli` | OpenClaw | URL 内容提取，LLM 友好格式输出 |
| `defuddle` | kepano | 网页清洁提取，去除广告和导航，节省 token |
| `doc` | Codex | 创建和编辑 .docx Word 文档 |
| `doc-coauthoring` | Anthropic | 结构化协同文档撰写工作流 |
| `slides` | Codex | 创建和编辑 .pptx 演示文稿（PptxGenJS）|
| `xlsx` | Anthropic | 电子表格读写、公式、图表（python-openpyxl）|
| `skywork-document` | Codex | 通过 Skywork API 生成多格式文档 |
| `notebooklm` | 社区 | 桥接 Google NotebookLM，source-grounded 引用级回答 |
| `interview-transcription` | 本机 | 访谈音频转写全流程：ASR 路线选择 + 说话人分离 + 整理 |
| `qiao-epub-bot` | 社区 | Telegram Z-Lib Bot 电子书下载，默认 epub，自动备选格式 |

### 二·五类：咨询与研究型（9个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `ljg-rank` | lijigang | 降秩引擎：给领域找出底层独立驱动力，砍到不可再少的生成器 |
| `ljg-roundtable` | lijigang | 圆桌讨论：以求真为目标的结构化多人辩证对话框架 |
| `ljg-paper` | lijigang | 论文阅读器：为非学术人士提取论文洞察，重理解不重批判 |
| `ljg-invest` | lijigang | 投资/行业分析：判断项目是否是"秩序创造机器" |
| `ljg-writes` | lijigang | 写作引擎：带着一个观点出发，在写的过程中把它想透 |
| `ljg-learn` | lijigang | 概念解剖：从8个维度切开一个概念，压成一句顿悟 |
| `ljg-plain` | lijigang | 白话引擎：把任何内容改写到聪明的十二岁小孩也能懂 |
| `ljg-card` | lijigang | 内容铸卡：将内容转为 PNG 视觉卡片（需 Playwright）|
| `doc-qa` | 本机 | 文稿快校：问题驱动，只输出实际存在的问题，按优先级排列 |

### 三类：开发工具型 · 编码 Agent 专用（25个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `chrome-cdp` | Codex | Chrome DevTools Protocol 本地浏览器控制 |
| `opencli` | jackwener | 50+ 网站/App 适配器，CDP 驱动，复用 Chrome 登录态 |
| `cc-connect` | 本机 | 管理 cc-connect 本地桥接服务，将 Claude Code 接入外部工具链 |
| `apify-data-pipeline` | Codex | Apify Actor 数据爬取与本地存储管道 |
| `glm-ocr-pdf` | 本机 | PDF 双模路由：原生提取 + 本机 GLM-OCR（Apple Silicon）|
| `gstack-review` | garrytan | PR 落地前代码审查：SQL 安全、LLM 信任边界、条件副作用 |
| `create-skill` | Cursor | 在 Cursor 中快速创建新 Skill |
| `create-rule` | Cursor | 在 Cursor 中创建项目规则文件 |
| `create-subagent` | Cursor | 创建独立子 Agent 处理复杂任务 |
| `shell` | Cursor | 安全的 Shell 命令执行封装 |
| `json-canvas` | kepano | Obsidian Canvas 文件（.canvas）创建与编辑 |
| `obsidian-cli` | kepano | Obsidian vault 读写、搜索、任务管理、插件调试 |
| `obsidian-markdown` | kepano | Obsidian 风格 Markdown（callouts/embeds/properties）|
| `obsidian-bases` | kepano | Obsidian Bases 数据库视图，含 FUNCTIONS_REFERENCE |
| `test-driven-development` | 社区 | 测试驱动开发，先写测试再写实现 |
| `systematic-debugging` | 社区 | 遇到 bug 时的系统化调试流程 |
| `writing-plans` | 社区 | 多步任务开始前先写实施计划 |
| `writing-skills` | 社区 | 新建或编辑 Skill，部署前验证 |
| `executing-plans` | 社区 | 在独立会话中执行已写好的实施计划 |
| `subagent-driven-development` | 社区 | 用独立子 Agent 并行执行实施计划 |
| `using-git-worktrees` | 社区 | 创建隔离的 git worktree 进行功能开发 |
| `requesting-code-review` | 社区 | 完成实现后请求代码审查 |
| `receiving-code-review` | 社区 | 收到代码审查反馈后的处理流程 |
| `verification-before-completion` | 社区 | 声称完成前必须运行验证命令确认结果 |
| `finishing-a-development-branch` | 社区 | 开发完成后的分支整合决策指引 |

---

## 平台 Overlay 说明

| Overlay | 文件 | 用途 |
|---------|------|------|
| `overlays/codex/` | `agents/openai.yaml` | Codex Agent 模型与工具配置（7 个 skill）|
| `overlays/hermes/` | hermes 专属配置 | Hermes 分类目录结构适配 |

---

## 日常维护

```bash
# 新增 skill
mkdir -p skills/my-skill && vim skills/my-skill/SKILL.md
git add . && git commit -m "feat: add my-skill" && git push
./scripts/sync-skills.sh

# 更新已有 skill
vim skills/commit/SKILL.md
git add . && git commit -m "fix: update commit skill" && git push
./scripts/sync-skills.sh

# 拉取最新并同步本机
cd ~/ai-skill && git pull && ./scripts/sync-skills.sh
```

---

## License

MIT
