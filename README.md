# ai-skill

> 🧠 跨平台 AI Skills 统一仓库 | by [@tommy-wangbot](https://github.com/tommy-wangbot)

本仓库收录了来自 Claude Code、Alma、OpenClaw、Codex、Cursor 等多个 AI 平台的精选 Skills，经过分类整理后统一管理，支持通过 [SkillUse](https://skilluse.dev) 一键安装到任意 Agent 平台。

---

## 📦 快速安装

### 前置条件

```bash
npm install -g skilluse
skilluse login
skilluse repo add tommy-wangbot/ai-skill --default
```

### 安装单个 Skill

```bash
skilluse install <skill-name>          # 安装到当前项目
skilluse install <skill-name> -g       # 全局安装
```

### 或通过 URL 直接安装

```bash
skilluse install https://github.com/tommy-wangbot/ai-skill/tree/main/.claude/skills/<skill-name>
```

---

## 🗂️ Skills 目录（共 30 个）

### 一类：通用型 · 推荐全平台安装（14个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `commit` | Claude | 生成 Conventional Commits 规范提交信息 |
| `epic` | Claude | 创建和管理 Epic 大型功能集合 |
| `issue` | Claude | 创建和管理本地 Issue 任务 |
| `publish` | Claude | 通过 GitHub Actions 发布新版本 |
| `plan-mode` | Alma | 进入结构化规划模式 |
| `todo` | Alma | 基于 Markdown 文件的任务清单管理 |
| `tasks` | Alma | 跨会话的多步骤全局任务追踪 |
| `memory-management` | Alma | 搜索和管理历史对话记忆 |
| `web-search` | Alma | 联网搜索最新信息 |
| `web-fetch` | Alma | 抓取和读取网页内容 |
| `find-skills` | OpenClaw | 智能发现和推荐可安装的 Skills |
| `multi-search-engine` | OpenClaw | 17 个搜索引擎，无需 API Key |
| `self-improving-agent` | OpenClaw | 持续捕获错误和改进经验 |
| `prompt-optimizer` | Codex | 将模糊 Prompt 优化为稳定可靠的指令 |

### 二类：内容处理型 · 按需安装（10个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `baoyu-translate` | Codex | 三模式翻译：快速 / 普通 / 精翻 |
| `tech-translation-expert` | Codex | 模仿宝玉风格的技术文章中英互译 |
| `baoyu-format-markdown` | Codex | Markdown 格式化与美化 |
| `baoyu-url-to-markdown` | Codex | 网页转 Markdown（支持需登录页面）|
| `baoyu-danger-x-to-markdown` | Codex | X/Twitter 推文转 Markdown |
| `wechat-to-markdown` | Codex | 微信公众号文章转 Markdown + 图片下载 |
| `jina-cli` | OpenClaw | URL 内容提取，LLM 友好格式输出 |
| `doc` | Codex | 创建和编辑 .docx Word 文档 |
| `slides` | Codex | 创建和编辑 .pptx 演示文稿 |
| `skywork-document` | Codex | 通过 Skywork API 生成多格式文档 |

### 三类：开发工具型 · 编码 Agent 专用（6个）

| Skill | 来源 | 功能描述 |
|-------|------|---------|
| `chrome-cdp` | Codex | 通过 Chrome DevTools Protocol 控制本地浏览器 |
| `apify-data-pipeline` | Codex | Apify Actor 数据爬取与本地存储管道 |
| `create-skill` | Cursor | 在 Cursor 中快速创建新 Skill |
| `create-rule` | Cursor | 在 Cursor 中创建项目规则文件 |
| `create-subagent` | Cursor | 创建独立子 Agent 处理复杂任务 |
| `shell` | Cursor | 安全的 Shell 命令执行封装 |

---

## 🌐 支持的 Agent 平台

通过 `skilluse agent <platform>` 切换平台，Skills 自动适配格式：

| 平台 | 切换命令 |
|------|---------|
| Claude Code | `skilluse agent claude` |
| Cursor | `skilluse agent cursor` |
| Windsurf | `skilluse agent windsurf` |
| GitHub Copilot | `skilluse agent github-copilot` |

---

## 🔄 常用命令

```bash
# 查看仓库内所有可用 skill
skilluse repo skills

# 搜索 skill
skilluse search <keyword>

# 更新已安装的所有 skill
skilluse upgrade

# 卸载 skill
skilluse uninstall <skill-name>

# 查看 skill 详情
skilluse info <skill-name>
```

---

## 📝 License

MIT
