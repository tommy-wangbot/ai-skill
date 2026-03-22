# ai-skill

> 🧠 跨平台 AI Skills 统一仓库 | by [@tommy-wangbot](https://github.com/tommy-wangbot)

GitHub 仓库 = 唯一 source of truth。  
公共 skill 内容放在 `skills/`，平台专属配置放在 `overlays/`，  
由 `scripts/sync-skills.sh` 合并生成到各平台的运行时目录。

---

## 仓库结构

```
ai-skill/
├── skills/                  # 公共 skill 内容（平台无关）
│   ├── commit/SKILL.md
│   ├── baoyu-translate/
│   │   ├── SKILL.md
│   │   └── references/
│   └── ...
├── overlays/                # 平台专属补丁（同名文件覆盖公共内容）
│   ├── codex/
│   │   ├── chrome-cdp/agents/openai.yaml
│   │   ├── doc/agents/openai.yaml
│   │   └── ...
│   └── openclaw/
│       ├── find-skills/.clawhub/
│       ├── multi-search-engine/_meta.json
│       └── self-improving-agent/hooks/
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

同步完成后，各平台直接加载对应运行时目录，无需任何额外配置。

| 平台 | 运行时目录 |
|------|-----------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/clawd/skills/` |

---

## Skills 目录（共 30 个）

### 一类：通用型（14个）

| Skill | 功能 |
|-------|------|
| `commit` | Conventional Commits 规范提交 |
| `epic` / `issue` / `publish` | 项目管理三件套 |
| `plan-mode` | 结构化规划模式 |
| `todo` / `tasks` | 任务与进度追踪 |
| `memory-management` | 历史对话记忆管理 |
| `web-search` / `web-fetch` | 联网搜索与网页抓取 |
| `find-skills` | 智能发现推荐 Skills |
| `multi-search-engine` | 17个搜索引擎，无需 API Key |
| `self-improving-agent` | 持续捕获错误与改进经验 |
| `prompt-optimizer` | Prompt 优化，支持多模型 |

### 二类：内容处理型（10个）

| Skill | 功能 |
|-------|------|
| `baoyu-translate` | 三模式翻译（快速/普通/精翻）|
| `tech-translation-expert` | 宝玉风格技术翻译 |
| `baoyu-format-markdown` | Markdown 格式化美化 |
| `baoyu-url-to-markdown` | 网页转 Markdown |
| `baoyu-danger-x-to-markdown` | X/Twitter 转 Markdown |
| `wechat-to-markdown` | 微信文章转 Markdown |
| `jina-cli` | URL 内容提取（LLM 友好）|
| `doc` / `slides` | Word / PPT 文档生成 |
| `skywork-document` | Skywork API 多格式文档 |

### 三类：开发工具型（6个）

| Skill | 功能 |
|-------|------|
| `chrome-cdp` | Chrome DevTools Protocol 控制 |
| `apify-data-pipeline` | Apify 数据爬取管道 |
| `create-skill` / `create-rule` | 创建 Skill / Rule |
| `create-subagent` / `shell` | 子 Agent 与 Shell 封装 |

---

## 更新 Skill

```bash
cd ~/ai-skill
# 编辑 skills/<name>/SKILL.md 或 overlays/<platform>/<name>/
git add . && git commit -m "feat: update <skill-name>"
git push

# 重新同步到本机
./scripts/sync-skills.sh
```

---

## 平台 overlay 说明

| overlay | 文件 | 用途 |
|---------|------|------|
| `overlays/codex/` | `agents/openai.yaml` | Codex Agent 配置 |
| `overlays/openclaw/` | `.clawhub/`, `_meta.json` | OpenClaw Hub 元数据 |
| | `config.json`, `metadata.json` | OpenClaw 运行配置 |
| | `.learnings/`, `hooks/`, `scripts/` | OpenClaw 自学习系统 |

---

## License

MIT
