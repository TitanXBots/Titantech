import os
import asyncio
import humanize
from pyrogram import Client , filters , __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery
from pyrogram.errors import FloodWait , UserIsBlocked , InputUserDeactivated
from bot import Bot
from config import *
from helper_func import subscribed , encode , decode , get_messages
from database.database import add_user , del_user , full_userbase , present_user
import logging
from pymongo import MongoClient

client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db["TelegramFiles"]

titanxofficials = FILE_AUTO_DELETE
titandeveloper = titanxofficials
file_auto_delete = humanize.naturaldelta(titandeveloper)

async def is_maintenance(client, user_id:int)->bool:
    check_msg = collection.find_one({"maintenance": "on"})
    if check_msg and user_id not in ADMINS:
        return True
    return False

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client , message: Message):
    user_id = message.from_user.id
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass 
    if await is_maintenance(client, user_id):
      await message.reply_text("Maintenance mode is currently active. Please try again later.")
      return
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" " , 1)[1]
        except IndexError:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception as e:
                print(f"Error parsing arguments: {e}")
                return
            if start <= end:
                ids = range(start , end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error parsing argument: {e}")
                return

        temp_msg = await message.reply("Wait Bro...")
        try:
            messages = await get_messages(client , ids)
        except Exception as e:
            print(f"Error getting messages: {e}")
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        titanx_msgs = []  # List to keep track of sent messages

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html ,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                titanx_msg = await msg.copy(chat_id=message.from_user.id , caption=caption , parse_mode=ParseMode.HTML ,
                                            reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                titanx_msgs.append(titanx_msg)

            except FloodWait as e:
                await asyncio.sleep(e.value)
                titanx_msg = await msg.copy(chat_id=message.from_user.id , caption=caption , parse_mode=ParseMode.HTML ,
                                            reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                titanx_msgs.append(titanx_msg)

            except Exception as e:
                print(f"Error copying message: {e}")
                pass

        k = await client.send_message(chat_id=message.from_user.id ,
                                      text=f"<b>❗️ <u>IMPORTANT</u> ❗️</b>\n\nThis Video / File Will Be Deleted In {file_auto_delete} (Due To Copyright Issues).\n\n📌 Please Forward This Video / File To Somewhere Else And Start Downloading There.")

        # Schedule the file deletion
        asyncio.create_task(delete_files(titanx_msgs , client , k))

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🧠 ʜᴇʟᴘ" , callback_data="help") ,
                    InlineKeyboardButton("🔰 ᴀʙᴏᴜᴛ" , callback_data="about")
                ] ,
                [
                    InlineKeyboardButton("💻 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ" , url="https://t.me/TitanOwner") ,
                    InlineKeyboardButton("🔐 ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ" , url="https://github.com/TitanXBots/FileStore-Bot")
                ] ,
                [
                    InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ʙᴏᴛ" , url="https://t.me/TitanXBackup/33")
                ] ,
                [
                    InlineKeyboardButton("☆ ᴍᴏᴠɪᴇ ʀᴇQᴜᴇꜱᴛ ɢʀᴏᴜᴘ ☆" , url="https://t.me/TitanMoviess")
                ] ,
                [
                    InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ" , url="https://t.me/TitanXBots") ,
                    InlineKeyboardButton("🔍 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ" , url="https://t.me/TitanMattersSupport")
                ]
            ]
        )
        await message.reply_photo(
            photo=START_PIC ,
            caption=START_MSG.format(
                first=message.from_user.first_name ,
                last=message.from_user.last_name ,
                username=None if not message.from_user.username else '@' + message.from_user.username ,
                mention=message.from_user.mention ,
                id=message.from_user.id
            ) ,
            reply_markup=reply_markup ,
        )
        return


# =====================================================================================##

WAIT_MSG = "<b>Working....</b>"

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"


# =====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client , message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ" , url=client.invitelink) ,
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ" , url=client.invitelink2) ,
        ] ,
        [
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ" , url=client.invitelink3) ,
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ" , url=client.invitelink4) ,
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='☢ ɴᴏᴡ ᴄʟɪᴄᴋ ʜᴇʀᴇ •' ,
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass
    if await is_maintenance(client, user_id):
      await message.reply_text("Maintenance mode is currently active. Please try again later.")
      return
    await message.reply_photo(
        photo=FORCE_PIC ,
        caption=FORCE_MSG.format(
            first=message.from_user.first_name ,
            last=message.from_user.last_name ,
            username=None if not message.from_user.username else '@' + message.from_user.username ,
            mention=message.from_user.mention ,
            id=message.from_user.id
        ) ,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot , message: Message):
    msg = await client.send_message(chat_id=message.chat.id , text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot , message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


async def delete_files(messages , client , k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id , message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

        # Safeguard against k.command being None or having insufficient parts
    command_part = k.command[1] if k.command and len(k.command) > 1 else None

    if command_part:
        button_url = f"https://t.me/{client.username}?start={command_part}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!" , url=button_url)]
            ]
        )
    else:
        keyboard = None

        # Edit message with the button
        try:
            await k.edit_text("Your Video / File Is Successfully Deleted ✅" , reply_markup=keyboard)
        except Exception as e:
            logging.error(f"Error editing the message: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")




# Replace with your log channel ID
LOG_CHANNEL_ID = "-1002313688533"  # The chat ID of the log channel (can be found from @username or by ID)

def format_new_user_message(user_id, user_name):
    NEW_USER_TXT = """
≈ ɪᴅ:- {}
≈ ɴᴀᴍᴇ:- {}"""
    
    return NEW_USER_TXT.format(user_id, user_name)

async def send_log_message(user_id, user_name):
    message = format_new_user_message(user_id, user_name)
    await app.send_message(LOG_CHANNEL_ID, message)

@Client.on_message(filters.new_chat_members)
async def new_member_handler(client, message):
    for new_member in message.new_chat_members:
        user_id = new_member.id
        user_name = new_member.first_name
        await send_log_message(user_id, user_name)

# Start the client
app = Client("my_bot")  # Replace with your session name or parameters

if __name__ == "__main__":  # Corrected from if name == "main":
    app.run()
