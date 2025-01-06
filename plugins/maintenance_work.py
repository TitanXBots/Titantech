from pyrogram import Client, filters
from pyrogram.types import *
import os
from os import environ
import re
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


id_pattern = re.compile(r'^.\d+$')


ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5356695781').split()]


async def convertmsg(msg: str) -> str:
    words = msg.lower().split()
    if len(words) > 1:
        return " ".join(words[1:])
    else:
        return ""

async def checkmsg(msg: str) -> bool:
    if msg == 'on':
        return True
    elif msg == 'off':
        return False
    else:
        return None

@Client.on_message(filters.command("maintenance") & filters.user(ADMINS))
async def maintenance(client: Client, message: Message):
    user_id = message.from_user.id
    m = message.text

    if not message.text.split()[1:]:
        await message.reply_text("Correct the command format. Usage: /maintenance [on/off]")
        return

    msg = await convertmsg(m)
    status = await checkmsg(msg)

    if status is True:
        check_msg = collection.find_one({"admin_id": user_id})
        if check_msg:
            on_off = check_msg["maintenance"]
            if on_off == 'on':
                await message.reply_text("Maintenance mode is already on.")
            elif on_off == 'off':
                collection.update_one({"admin_id": user_id}, {"$set": {"maintenance": "on"}})
                await message.reply_text("Maintenance mode turned on.")
        else:
            collection.insert_one({"admin_id": user_id, "maintenance": "on"})
            await message.reply_text("Maintenance mode turned on (new entry).")
    elif status is False:
        check_msg1 = collection.find_one({"admin_id": user_id})
        if check_msg1:
            on_off1 = check_msg1["maintenance"]
            if on_off1 == 'off':
                await message.reply_text("Maintenance mode is already off.")
            elif on_off1 == 'on':
                collection.update_one({"admin_id": user_id}, {"$set": {"maintenance": "off"}})
                await message.reply_text("Maintenance mode turned off.")
        else:
            collection.insert_one({"admin_id": user_id, "maintenance": "off"})
            await message.reply_text("Maintenance mode turned off (new entry).")
    else:
        await message.reply_text("None")

@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
  user_id = message.from_user.id
  check_msg = collection.find_one({"admin_id": user_id})
  if check_msg and user_id not in ADMINS:
      on_off = check_msg["maintenance"]
      if on_off == 'on':
          await message.reply_text("Maintenance mode is currently active. Please try again later.")
      else:
          await message.reply_text("Welcome to the bot!")
  else:
      await message.reply_text("Welcome to the bot!")

print("Running")
user.run()
