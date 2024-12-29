
import logging
from bot import Bot
import datetime
from pyrogram import Client, filters

# Replace 'LOG_CHANNEL_ID' with your log channel's ID
LOG_CHANNEL_ID = '-1002132998073'


RESTART_TXT = """
Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

📅 Dᴀᴛᴇ : {}
⏰ Tɪᴍᴇ : {}
🌐 Tɪᴍᴇᴢᴏɴᴇ : Asia/Kolkata
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: v2.7.1 [ Sᴛᴀʙʟᴇ ]"""

@Client.on_message(filters.command("restart")) # You will use /restart command to trigger this event.
async def send_restart_message(client, message):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    formatted_text = RESTART_TXT.format(date_str, time_str)
    await client.send_message(message.chat.id, formatted_text)
