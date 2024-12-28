
import logging
from telegram import Bot
import datetime

# Replace 'YOUR_TOKEN' with your bot's API token
TOKEN = 'YOUR_TOKEN'
# Replace 'LOG_CHANNEL_ID' with your log channel's ID
LOG_CHANNEL_ID = '@your_log_channel'

# Initialize bot
bot = Bot(token=TOKEN)

def send_restart_message():
    # Current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    RESTART_TXT = f"""
Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

📅 Dᴀᴛᴇ : {date_str}
⏰ Tɪᴍᴇ : {time_str}
🌐 Tɪᴍᴇᴢᴏɴᴇ : Asia/Kolkata
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: v2.7.1 [ Sᴛᴀʙʟᴇ ]
"""

    # Send the message to the log channel
    bot.send_message(chat_id=LOG_CHANNEL_ID, text=RESTART_TXT, parse_mode='HTML')

if __name__ == "__main__":
    send_restart_message()
