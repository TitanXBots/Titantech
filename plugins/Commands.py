from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("id"))
async def id_command(client: Client, message: Message):
    if message.chat.type == "private":
       await message.reply_text(f"Your user ID is : {message.from_user.id}")
   



# --- Bot Run ---
if __name__ == "__main__":
    print("Bot Started...")
