
import asyncio
import re
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from typing import Dict, Optional

# --- Configuration ---
API_ID =  # Your API ID
API_HASH =  # Your API HASH
BOT_TOKEN =  # Your Bot Token
DATABASE_CHANNEL_ID =  # Your Database Channel ID (Integer)
ADMIN_IDS = [ ]  # List of admin user IDs (Integers)

# --- State Management ---
user_states: Dict[int, dict] = {}

# --- Regular Expression for Format Validation ---
FORMAT_REGEX = re.compile(r"^(\s*[0-9]+[pP](?:=| =)\s*\d+\s*(?:,\s*)?)+$", re.IGNORECASE)
RESOLUTION_REGEX = re.compile(r"([0-9]+[pP])(?:=| =)(\d+)", re.IGNORECASE)

# --- Pyrogram Client Setup ---
app = Client("link_generator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Admin Check Function ---
async def is_admin(client: Client, user_id: int) -> bool:
    return user_id in ADMIN_IDS

# --- Helper Function to Get a List of Messages ---
async def get_messages_from_post(client: Client, post_link: str) -> Optional[list[types.Message]]:
    try:
        match = re.match(r'https://t.me/(?P<channel>[^/]+)/(?P<message_id>\d+)', post_link)
        if not match:
            return None
        channel = match.group('channel')
        message_id = int(match.group('message_id'))

        if channel.startswith("-100"):  #If channel id
             channel_id = int(channel)
             if channel_id != DATABASE_CHANNEL_ID:
                return None
        else:
            try:
                chat = await client.get_chat(channel)
                channel_id = chat.id
                if channel_id != DATABASE_CHANNEL_ID:
                    return None
            except Exception:
                return None

        messages = []
        async for message in client.get_chat_history(channel_id,limit=1000):
          if message.id >= message_id:
              messages.append(message)
        return messages
    except UserNotParticipant:
       return None
    except Exception as e:
       print(e)
       return None

# --- /flink Command Handler ---
@app.on_message(filters.command("flink") & filters.private)
async def flink_command(client: Client, message: types.Message):
    user_id = message.from_user.id
    if not await is_admin(client, user_id):
        await message.reply("This command is only for admins.")
        return

    user_states[user_id] = {"state": "initial"}
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("sᴇᴛ ғᴏʀᴍᴀᴛ", callback_data="set_format")],
        [InlineKeyboardButton("sᴛᴀʀᴛ ᴘʀᴏᴄᴇss", callback_data="start_process")]
    ])
    await message.reply("Select an action:", reply_markup=markup)


# --- set_format Callback Handler ---
@app.on_callback_query(filters.regex("set_format"))
async def set_format_callback(client: Client, callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_states:
        await callback_query.answer("Please use /flink command first.")
        return

    user_states[user_id]["state"] = "waiting_for_format"
    await callback_query.message.edit_text("Please send the format string (e.g., `480P = 1, 720P = 2`):")
    await callback_query.answer()


# --- Format Input Handler ---
@app.on_message(filters.text & filters.private)
async def format_input(client: Client, message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id].get("state") != "waiting_for_format":
        return

    format_string = message.text
    if not FORMAT_REGEX.match(format_string):
        await message.reply("Invalid format string. Please follow the example `480P = 1, 720P = 2`.")
        return

    user_states[user_id]["format"] = format_string
    user_states[user_id]["state"] = "format_set"

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("sᴛᴀʀᴛ ᴘʀᴏᴄᴇss", callback_data="start_process")]
    ])
    await message.reply("Format set successfully! Now select the start process:", reply_markup=markup)


# --- start_process Callback Handler ---
@app.on_callback_query(filters.regex("start_process"))
async def start_process_callback(client: Client, callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_states:
        await callback_query.answer("Please use /flink command first.")
        return

    if user_states[user_id].get("state") != "format_set":
        await callback_query.answer("Please set the format first.")
        return

    user_states[user_id]["state"] = "waiting_for_post_link"
    await callback_query.message.edit_text("Please send the post link from the database channel.")
    await callback_query.answer()


# --- Post Link Handler ---
@app.on_message(filters.text & filters.private)
async def post_link_handler(client: Client, message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id].get("state") != "waiting_for_post_link":
        return

    post_link = message.text
    messages = await get_messages_from_post(client, post_link)

    if not messages:
        await message.reply("Invalid post link or access denied for database channel")
        return

    try:
        format_string = user_states[user_id].get("format")
        resolutions = {}
        for match in RESOLUTION_REGEX.finditer(format_string):
            resolution = match.group(1).upper()
            count = int(match.group(2))
            resolutions[resolution] = count

        link_texts = []
        available_messages = []
        for msg in messages:
          if msg.document:
            available_messages.append(msg)

        for resolution, count in resolutions.items():
          found = 0
          buttons = []
          for msg in available_messages:
              if found < count:
                if msg.document:
                   buttons.append(InlineKeyboardButton(f"{resolution} #{found+1}", url=f"https://t.me/c/{str(DATABASE_CHANNEL_ID).replace('-100','')}/{msg.id}"))
                   found += 1

          if buttons:
            link_texts.append(f"<b>{resolution}</b>\n")
            markup = InlineKeyboardMarkup([buttons[i:i + 2] for i in range(0, len(buttons), 2)])
            await message.reply(link_texts[-1], reply_markup=markup)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
       del user_states[user_id]  # Clear user state when process complete

# --- Refresh Button (Not fully implemented yet) ---
@app.on_callback_query(filters.regex("refresh_link"))
async def refresh_link_callback(client: Client, callback_query: types.CallbackQuery):
    # Implement logic to refresh links
    await callback_query.answer("Refresh functionality is not fully implemented yet.")

# --- Cancel Command Handler ---
@app.on_message(filters.text & filters.regex(r"^CANCEL$") & filters.private)
async def cancel_command(client: Client, message: types.Message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    await message.reply("Operation canceled.")

# --- Run the Client ---
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
