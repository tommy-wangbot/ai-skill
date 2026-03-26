---
name: qiao-epub-bot
description: Search and download ebooks via Telegram Z-Lib Bot channel. Trigger automatically when the user: (1) inputs a book title or author name, (2) says "download book", "find book", "get ebook", "下载书", "找书", "搜书", "帮我下载", "下载电子书", "epub", "pdf 下载", or provides a book name with author. Default format is epub. Saves to ~/Downloads/books/.
---

# qiao-epub-bot — Telegram Z-Lib 电子书下载

通过 Telegram Z-Lib Bot（Telethon 客户端）搜索和下载电子书。支持 epub、pdf、mobi 等格式。无需浏览器，直接在终端完成搜索和下载。

## 前置配置（首次使用）

### 1. 安装依赖

```bash
cd ~/.claude/skills/qiao-epub-bot
pip install -r requirements.txt
```

### 2. 配置 Telegram API

在 https://my.telegram.org 申请 API 凭证，然后编辑 `scripts/main.py` 顶部：

```python
API_ID   = 你的 api_id      # 整数
API_HASH = '你的 api_hash'  # 字符串
```

### 3. 首次登录（只需一次）

```bash
python3 ~/.claude/skills/qiao-epub-bot/scripts/main.py "任意书名"
```

终端会提示输入手机号和验证码，完成后 Session 文件保存在当前目录，后续无需重复登录。

---

## 使用方式

```bash
# 基本用法（默认 epub 格式）
python3 ~/.claude/skills/qiao-epub-bot/scripts/main.py "Show Your Work Austin Kleon"

# 指定格式
python3 ~/.claude/skills/qiao-epub-bot/scripts/main.py "Deep Work" --format pdf

# 指定保存目录
python3 ~/.claude/skills/qiao-epub-bot/scripts/main.py "穷查理宝典" --dir ~/Documents/books
```

## 工作流程

1. 通过 Telethon 连接 Telegram，检查登录状态
2. 向 Z-Lib Bot（`@gggitng_bot`）发送搜索关键词
3. 解析返回结果：
   - 有 Inline Buttons → 点击目标格式按钮
   - 纯文本列表含 `/book` 指令 → 发送下载指令
   - 收到文件消息 → 自动下载到本地目录
4. 保存至 `~/Downloads/books/`（默认），打印文件路径

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `query` | 必填 | 书名或作者，支持中英文 |
| `--format` | `epub` | 目标格式：epub / pdf / mobi |
| `--dir` | `~/Downloads/books` | 下载保存目录 |

## 注意事项

- Bot 用户名（`ZLIB_BOT_USERNAME`）可能随时变更，如失效请更新 `scripts/main.py` 顶部配置
- 超时限制 120 秒
- Session 文件请勿泄露（包含 Telegram 登录凭证）
- 仅供个人学习使用

## 当 Claude 调用时

当用户提供书名或请求下载书籍时，Claude 会：
1. 确认书名、格式（默认 epub）、保存目录
2. 执行 `python3 ~/.claude/skills/qiao-epub-bot/scripts/main.py "<书名>" --format <格式>`
3. 报告下载结果和文件路径
