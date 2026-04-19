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

<!-- SKILLS_START -->
## Skills 目录（共 72 个）

### 一类：通用型 · 推荐全平台安装（21个）

| Skill | 功能描述 |
|-------|---------|
| `commit` | Generate Conventional Commits 1 |
| `epic` | Create and manage Epics - collections of related issues for major feature areas |
| `issue` | Create and manage local Issue specs (specs/issues/) - individual work items with testable acceptance criteria |
| `publish` | Publish a new version via GitHub Actions |
| `plan-mode` | Switch into structured planning mode before outlining multi-step solutions |
| `todo` | Manage a structured task list using a Markdown file in the workspace |
| `tasks` | Global multi-step task tracking |
| `memory-management` | 管理对话记忆和历史记录 |
| `web-search` | Search the web for information using the built-in WebSearch tool |
| `web-fetch` | Fetch and read web pages |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X" |
| `multi-search-engine` | 多引擎联合搜索工具 |
| `self-improving-agent` | Captures learnings |
| `prompt-optimizer` | High-quality prompt optimization for turning vague or unstable prompts into reliable |
| `gstack-office-hours` | YC Office Hours — two modes |
| `gstack-retro` | Weekly engineering retrospective |
| `brainstorming` | 头脑风暴与创意探索 |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills |
| `fireworks-tech-graph` | 生成生产级 SVG+PNG 技术图表 |
| `diagram-generator` | 多格式图表生成工具 |

### 二类：内容处理型 · 按需安装（17个）

| Skill | 功能描述 |
|-------|---------|
| `baoyu-translate` | Translates articles and documents between languages with three modes - quick (direct) |
| `tech-translation-expert` | 将英文技术内容翻译为地道中文 |
| `baoyu-format-markdown` | Formats plain text or markdown files with frontmatter |
| `baoyu-url-to-markdown` | Fetch any URL and convert to markdown using Chrome CDP |
| `baoyu-danger-x-to-markdown` | Converts X (Twitter) tweets and articles to markdown with YAML front matter |
| `baoyu-youtube-transcript` | Downloads YouTube video transcripts/subtitles and cover images by URL or video ID |
| `wechat-to-markdown` | Convert WeChat public account article links (mp |
| `jina-cli` | A lightweight CLI tool wrapping Jina AI Reader API for fetching and parsing URLs into LLM-friendly formats (Markdown/Text/HTML) |
| `defuddle` | Extract clean markdown content from web pages using Defuddle CLI |
| `doc` | Use when the task involves reading |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation |
| `slides` | Create and edit presentation slide decks (` |
| `xlsx` | Use this skill any time a spreadsheet file is the primary input or output |
| `skywork-document` | Use when the task is to create a polished document in `docx` |
| `notebooklm` | Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded |
| `interview-transcription` | 访谈音频转写全流程系统：选择 ASR 路线运行转写、LLM 纠错、结构化阅读版生成、词库维护、评分表生成 |
| `qiao-epub-bot` |  |

### 二·五类：咨询与研究型（9个）

| Skill | 功能描述 |
|-------|---------|
| `ljg-rank` | 给一个领域 |
| `ljg-roundtable` | Structured roundtable discussion framework with a truth-seeking moderator who invites representative figures for dialectical debate on any topic |
| `ljg-paper` | Paper reader for non-academics |
| `ljg-invest` | 投资分析 |
| `ljg-writes` | 写作引擎 |
| `ljg-learn` | Deep concept anatomist that deconstructs any concept through 8 exploration dimensions (history |
| `ljg-plain` | Cognitive atom: Plain (白) |
| `ljg-card` | Content caster (铸) |
| `doc-qa` | 文稿快校 |

### 三类：开发工具型 · 编码 Agent 专用（25个）

| Skill | 功能描述 |
|-------|---------|
| `chrome-cdp` | Inspect or interact with pages already open in the local Chrome browser via Chrome DevTools Protocol |
| `opencli` | OpenCLI — Make any website or Electron App your CLI |
| `cc-connect` | 管理 cc-connect 本地桥接服务 |
| `apify-data-pipeline` | Run Apify Actors from Codex with a repeatable pipeline (discover actor |
| `glm-ocr-pdf` | Use local PDF-native tools plus the local GLM-OCR install on this machine to work with PDF files |
| `gstack-review` | Pre-landing PR review |
| `create-skill` | Guides users through creating effective Agent Skills for Cursor |
| `create-rule` | Create Cursor rules for persistent AI guidance |
| `create-subagent` | Create custom subagents for specialized AI tasks |
| `shell` | Runs the rest of a /shell request as a literal shell command |
| `json-canvas` | Create and edit JSON Canvas files ( |
| `obsidian-cli` | Interact with Obsidian vaults using the Obsidian CLI to read |
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown with wikilinks |
| `obsidian-bases` | Create and edit Obsidian Bases ( |
| `test-driven-development` | Use when implementing any feature or bugfix |
| `systematic-debugging` | Use when encountering any bug |
| `writing-plans` | 制定多步骤任务的详细执行计划 |
| `writing-skills` | Use when creating new skills |
| `executing-plans` | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification |
| `requesting-code-review` | Use when completing tasks |
| `receiving-code-review` | Use when receiving code review feedback |
| `verification-before-completion` | Use when about to claim work is complete |
| `finishing-a-development-branch` | Use when implementation is complete |

<!-- SKILLS_END -->

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
