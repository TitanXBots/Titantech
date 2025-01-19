
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS

# A set to hold banned user IDs
banned_users = set()

# Command to ban a user
@Client.on_message(filters.command("ban") & filters.user("ADMINS"))
def ban_user(client, message: Message):
    if len(message.command) < 2:
        message.reply_text("Usage: /ban ")
        return

    user_id = int(message.command[1])
    banned_users.add(user_id)
    message.reply_text(f"User {user_id} has been banned.")

# Command to unban a user
@Client.on_message(filters.command("unban") & filters.user("ADMINS"))
def unban_user(client, message: Message):
    if len(message.command) < 2:
        message.reply_text("Usage: /unban ")
        return

    user_id = int(message.command[1])
    if user_id in banned_users:
        banned_users.remove(user_id)
        message.reply_text(f"User {user_id} has been unbanned.")
    else:
        message.reply_text(f"User {user_id} is not banned.")
