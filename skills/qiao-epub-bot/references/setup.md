# 首次配置指南

## 获取 Telegram API 凭证

1. 访问 https://my.telegram.org
2. 登录你的 Telegram 账号
3. 点击「API development tools」
4. 填写应用名称（随意）和平台（Desktop）
5. 获得 `api_id`（整数）和 `api_hash`（字符串）

## 更新配置

编辑 `scripts/main.py` 第 7-8 行：

```python
API_ID   = 123456          # 替换为你的 api_id
API_HASH = 'abc123...'    # 替换为你的 api_hash
```

## 更换 Z-Lib Bot

如果当前 Bot（`@gggitng_bot`）失效，在 Telegram 搜索「zlib」找到存活的 Bot，
更新 `scripts/main.py` 第 9 行：

```python
ZLIB_BOT_USERNAME = '@新的bot用户名'
```

## Session 文件位置

首次登录后，Session 文件保存在运行命令时的当前目录：
```
qiao_zlib_session.session
```

建议固定在一个目录运行，避免重复登录。
