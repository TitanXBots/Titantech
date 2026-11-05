
import asyncio
import time

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from database.database import get_all_users, is_admin


# Auto-delete time: 24 hours
DELETE_AFTER_SECONDS = 24 * 60 * 60


async def delete_later(client, chat_id, message_id):
    """Automatically delete a broadcast message after the set time."""
    await asyncio.sleep(DELETE_AFTER_SECONDS)

    try:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
    except Exception as e:
        print(f"Auto-delete failed for {chat_id}: {e}")


async def send_broadcast(client, message, mode):

    if not await is_admin(message.from_user.id):
        return await message.reply_text("⚠️ ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ!")

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ.</b>"
        )

    users = await get_all_users()
    broadcast_msg = message.reply_to_message

    status_msg = await message.reply_text(
        "<b>📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ...</b>"
    )

    start_time = time.time()

    success = 0
    failed = 0
    pinned = 0
    total = len(users)

    for user_id in users:
        try:
            sent_msg = await broadcast_msg.copy(chat_id=user_id)

            success += 1

            # Auto-delete broadcast
            if mode == "delete":
                asyncio.create_task(
                    delete_later(
                        client,
                        user_id,
                        sent_msg.id
                    )
                )

            # Pin broadcast
            elif mode == "pin":
                try:
                    await client.pin_chat_message(
                        chat_id=user_id,
                        message_id=sent_msg.id,
                        disable_notification=True
                    )
                    pinned += 1

                except Exception as e:
                    print(f"Pin failed for {user_id}: {e}")

        except FloodWait as e:
            await asyncio.sleep(e.value)

            try:
                sent_msg = await broadcast_msg.copy(chat_id=user_id)
                success += 1

                if mode == "delete":
                    asyncio.create_task(
                        delete_later(client, user_id, sent_msg.id)
                    )

                elif mode == "pin":
                    try:
                        await client.pin_chat_message(
                            chat_id=user_id,
                            message_id=sent_msg.id,
                            disable_notification=True
                        )
                        pinned += 1
                    except Exception:
                        pass

            except Exception:
                failed += 1

        except Exception as e:
            print(f"Broadcast failed for {user_id}: {e}")
            failed += 1

        await asyncio.sleep(0.1)

    elapsed = int(time.time() - start_time)

    result = (
        "<b>📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n\n"
        f"👥 <b>ᴛᴏᴛᴀʟ:</b> <code>{total}</code>\n"
        f"✅ <b>ꜱᴜᴄᴄᴇꜱꜱ:</b> <code>{success}</code>\n"
        f"❌ <b>ꜰᴀɪʟᴇᴅ:</b> <code>{failed}</code>\n"
    )

    if mode == "delete":
        result += (
            f"🗑 <b>ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ:</b> <code>24 Hours</code>\n"
        )

    elif mode == "pin":
        result += (
            f"📌 <b>ᴘɪɴɴᴇᴅ:</b> <code>{pinned}</code>\n"
        )

    result += f"⏱ <b>ᴛɪᴍᴇ:</b> <code>{elapsed}s</code>"

    await status_msg.edit_text(result)


# Normal broadcast
@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client: Client, message: Message):
    await send_broadcast(client, message, "normal")


# Auto-delete broadcast
@Client.on_message(filters.command("dbroadcast") & filters.private)
async def dbroadcast_handler(client: Client, message: Message):
    await send_broadcast(client, message, "delete")


# Pin broadcast
@Client.on_message(filters.command("pbroadcast") & filters.private)
async def pbroadcast_handler(client: Client, message: Message):
    await send_broadcast(client, message, "pin")
  
