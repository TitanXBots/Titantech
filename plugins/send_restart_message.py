import logging
import datetime
import os
from pyrogram import Client, filters
# Configuration (Move to a config file/environment variables for production)
LOG_CHANNEL_ID = '-1002132998073'  # Replace with your log channel ID

RESTART_TXT = """
Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

📅 Dᴀᴛᴇ : {}
⏰ Tɪᴍᴇ : {}
🌐 Tɪᴍᴇᴢᴏɴᴇ : Asia/Kolkata
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: v2.7.1 [ Sᴛᴀʙʟᴇ ]"""

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("restart") & filters.private)
async def send_restart_message(client, message):
    try:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        formatted_text = RESTART_TXT.format(date_str, time_str)

        # Send restart message to the user
        await Client.send_message(message.chat.id, formatted_text)
        logger.info(f"Restart command received from user {message.from_user.id} in chat {message.chat.id}. Sending restart message.")

        # Send restart message to the log channel (optional)
        if LOG_CHANNEL_ID:
            try:
                await Client.send_message(LOG_CHANNEL_ID, formatted_text)
                logger.info(f"Sent restart notification to the log channel {LOG_CHANNEL_ID}")
            except Exception as e:
               logger.error(f"Failed to send restart notification to the log channel: {e}")

        # Perform the actual restart (using os.execv)
        logger.info("Initiating bot restart.")
        await message.reply_text("Bot is restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)  # Use sys.executable and sys.argv for correct restart

    except Exception as e:
        logger.error(f"Error processing restart command: {e}")
        await client.send_message(
            message.chat.id,
            "An error occurred during restart. Please check the logs.",
        )

if __name__ == '__main__':
    import sys
