import asyncio
import argparse
import os
import re
from telethon import TelegramClient, events
from telethon.tl.custom import Message

# =============== 配置区 ===============
# 替换为你自己在 https://my.telegram.org 申请的 API 认证信息
API_ID = 2040  # 默认占位值，用户需替换
API_HASH = 'b18441a1ff607e10a989891a5462e627' # 默认占位值，用户需替换
ZLIB_BOT_USERNAME = '@gggitng_bot' # 根据目前存活的 Z-Lib Bot 替换
SESSION_NAME = 'qiao_zlib_session'

async def download_book(client: TelegramClient, entity, query: str, target_format: str, out_dir: str):
    print(f"🔍 搜索: {query}")
    
    os.makedirs(out_dir, exist_ok=True)
    file_received = asyncio.get_event_loop().create_future()
    
    @client.on(events.NewMessage(chats=entity))
    async def handler(event: events.NewMessage.Event):
        msg: Message = event.message
        
        # 场景一：收到文件
        if msg.document:
            size_mb = msg.file.size / 1024 / 1024
            print(f"📥 收到文件: {msg.file.name} ({size_mb:.2f} MB)")
            print("⏳ 正在下载...")
            file_path = await client.download_media(msg, file=out_dir)
            print(f"✅ 保存成功: {file_path}")
            if not file_received.done():
                file_received.set_result(file_path)
            return

        # 场景二：收到搜索结果（带有 Inline Buttons）
        # 注意：ZLib bot 的分页按钮没必要阻挡后续纯文本分析
        if msg.buttons:
            all_buttons = [b for row in msg.buttons for b in row]
            fallback_button = None

            for button in all_buttons:
                text_lower = button.text.lower()
                if target_format.lower() in text_lower:
                    # 找到目标格式，直接点击
                    size_match = re.search(r'(\d+(\.\d+)?\s?[mM][bB])', button.text)
                    size_str = size_match.group(1) if size_match else "未知大小"
                    print(f"📚 选择: {target_format} ({size_str})")
                    print("📥 请求下载...")
                    await button.click()
                    return
                # 记录第一个含下载格式关键词的按钮作为备选
                if fallback_button is None and re.search(r'\b(pdf|mobi|fb2|djvu|azw3?|txt|zip)\b', text_lower):
                    fallback_button = button

            # 目标格式不存在，启用备选格式
            if fallback_button:
                size_match = re.search(r'(\d+(\.\d+)?\s?[mM][bB])', fallback_button.text)
                size_str = size_match.group(1) if size_match else "未知大小"
                print(f"⚠️  未找到 {target_format}，改用备选格式: {fallback_button.text.strip()} ({size_str})")
                print("📥 请求下载...")
                await fallback_button.click()
                return

            # 没有任何下载按钮，继续走纯文本解析
            print("💬 存在附加按钮：", [b.text for b in all_buttons])
            
        # 场景三：收到纯文本形式的结果列表
        if msg.text and '/book' in msg.text:
            lines = msg.text.split('\n')
            fallback_command = None

            for line in lines:
                if '/book' not in line and '/zlib' not in line:
                    continue
                match = re.search(r'(/[\w\d_]+)', line)
                if not match:
                    continue
                command = match.group(1)
                if target_format.lower() in line.lower():
                    # 找到目标格式，直接发送
                    print(f"📚 选择: {target_format} -> {command}")
                    print("📥 请求下载...")
                    await client.send_message(entity, command)
                    return
                # 记录第一个可用格式行作为备选
                if fallback_command is None:
                    fallback_command = (command, line.strip())

            # 目标格式不存在，启用备选格式
            if fallback_command:
                command, desc = fallback_command
                print(f"⚠️  未找到 {target_format}，改用备选: {desc}")
                print("📥 请求下载...")
                await client.send_message(entity, command)
                return

            print(f"❌ 文字结果中未找到任何可下载格式。")
            if not file_received.done():
                file_received.set_result(None)
            return

    # 1. 发送关键词
    await client.send_message(entity, query)
    
    # 2. 等待文件返回 (120秒超时)
    try:
        result = await asyncio.wait_for(file_received, timeout=120.0)
    except asyncio.TimeoutError:
        print("❌ 请求超时，未能下载文件。(timeout 2m)")
    finally:
        client.remove_event_handler(handler)

async def main():
    parser = argparse.ArgumentParser(description="Z-Lib 电子书下载机器人 (Telethon 核心)")
    parser.add_argument('query', type=str, nargs='+', help="书名或作者 (如: Show Your Work Austin Kleon)")
    parser.add_argument('--format', type=str, default='epub', help="希望下载的格式 (默认为 epub)")
    parser.add_argument('--dir', type=str, default=os.path.expanduser('~/Downloads/books'), help="下载保存目录")
    
    args = parser.parse_args()
    query_str = " ".join(args.query)
    
    # 初始化客户端
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    # 我们不希望在 Claude Code 运行时一直卡在等待验证码
    # 但如果是手动运行，需要进入登录流程
    await client.connect()
    if not await client.is_user_authorized():
        print("⚠️ 未授权或未登录。正在启动交互式登录流程...")
        # 这将会在终端提示你输入手机号和验证码
        await client.start()
    
    entity = await client.get_entity(ZLIB_BOT_USERNAME)
    
    await download_book(client, entity, query_str, args.format, args.dir)
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
