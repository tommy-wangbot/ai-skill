---
name: cc-connect
description: 管理 cc-connect 本地桥接服务，将 Claude Code / Codex / OpenClaw 三个 Agent 与 Telegram / 飞书等消息平台打通。当用户提到"启动 cc-connect"、"停止 cc-connect"、"查看会话"、"切换 Agent"、"Telegram 连不上"、"配置 Bot"、"cc-connect 状态"时使用此 skill。
---

# cc-connect 管理

cc-connect 是一个本地守护进程，把 AI Agent（Claude Code、Codex、OpenClaw）桥接到 Telegram / 飞书等消息平台。

## 配置文件

```
~/.cc-connect/config.toml   ← 主配置（agent + 平台 token）
~/.cc-connect/              ← 会话数据（JSON 文件）
```

当前项目配置：
- `claude-consulting` → claudecode → `/Users/tommy/Documents/claude` → Telegram
- `codex-research`    → codex      → `/Users/tommy/Documents/codex`  → Telegram
- `openclaw-main`     → acp        → `/Users/tommy/clawd`            → Telegram（待启用）

---

## 守护进程管理

```bash
# 启动（后台常驻）
cc-connect daemon start

# 查看状态
cc-connect daemon status

# 查看实时日志
cc-connect daemon logs -f

# 停止 / 重启
cc-connect daemon stop
cc-connect daemon restart

# 安装为 macOS launchd 服务（开机自启）
cc-connect daemon install
cc-connect daemon uninstall
```

---

## Telegram 常用命令

在 Telegram 中发送给 Bot：

| 命令 | 功能 |
|------|------|
| `/new [名称]` | 新建会话 |
| `/list` | 列出所有会话 |
| `/switch [名称]` | 切换会话 |
| `/whoami` | 获取你的 User ID（用于 admin_from 配置）|
| `/status` | 查看当前会话状态 |
| `/dir [路径]` | 切换工作目录（需 admin_from） |
| `/mode [模式]` | 切换权限模式：default/auto/yolo |
| `/quiet` | 切换静默模式（隐藏工具调用过程）|
| `/compress` | 压缩上下文 |
| `/restart` | 重启 Agent 会话 |

---

## 初始化步骤（首次使用）

1. **新建 Telegram Bot**：前往 @BotFather → `/newbot` → 获取 token
2. **填入配置**：编辑 `~/.cc-connect/config.toml`，替换 `YOUR_NEW_BOT_TOKEN`
3. **获取 User ID**：启动后向 bot 发 `/whoami`，将返回的 ID 填入 `admin_from`
4. **启动服务**：`cc-connect daemon start`
5. **验证**：向 bot 发任意消息，应收到 Claude Code 的响应

---

## 常见问题

**Bot 无响应** → `cc-connect daemon logs -f` 查看错误；检查 token 是否正确

**与 OpenClaw 冲突** → cc-connect 和 OpenClaw 不能共用同一个 Telegram Bot token（均使用 long polling），必须分别创建 bot

**OpenClaw 接入** → 若 OpenClaw 实现了 ACP 协议，在 config.toml 中取消注释 `openclaw-main` 项目，agent type 填 `acp`

**切换工作目录** → Telegram 发送 `/dir /Users/tommy/Documents/codex/interview_transcription_eval`
