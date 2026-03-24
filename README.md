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
│   └── openclaw/            # .clawhub/ + _meta.json + hooks/ + scripts/
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
./scripts/sync-skills.sh openclaw
```

| 平台 | 运行时目录 |
|------|-----------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/clawd/skills/` |

---

## Skills 目录（共 44 个）

### 一类：通用型 · 推荐全平台安装（16个）

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

### 二类：内容处理型 · 按需安装（16个）

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
| `asr` | ListenHub | 本地语音转文字，sensevoice 模型，无需 API Key |

### 三类：开发工具型 · 编码 Agent 专用（12个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `chrome-cdp` | Codex | Chrome DevTools Protocol 本地浏览器控制 |
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

---

## 平台 Overlay 说明

| Overlay | 文件 | 用途 |
|---------|------|------|
| `overlays/codex/` | `agents/openai.yaml` | Codex Agent 模型与工具配置（7 个 skill）|
| `overlays/openclaw/` | `.clawhub/`, `_meta.json` | OpenClaw Hub 元数据（3 个 skill）|
| | `.learnings/`, `hooks/`, `scripts/` | OpenClaw 自学习与 Hook 系统 |

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
