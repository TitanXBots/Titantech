from pyrogram import Client, filter
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

ADMIN_IDS = [5356695781]  # Or load from env vars

app = Client("my_bot")  # Replace with your bot's name or session string


@Client.on_message(filters.command("id"))
async def id_command(client, message):  # Add async
logging.info(f"Received /id command from user: {message.from_user.id}")
try:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"

    await message.reply_text(f"Your User ID is: {user_id}")  # Use await

    await client.send_message(ADMIN_IDS[0], f"{user_name} (User ID: {user_id}) has requested their ID.")  # Use await

    if user_id in ADMIN_IDS:
        await message.reply_text(f"You are an admin! Admin User ID is: {ADMIN_IDS}")  # Use await
except Exception as e:
    logging.error(f"Error processing /id command: {e}")
    await message.reply_text("An error occurred. Please try again later.")  # Use await


async def main():
    await app.start()
    print("Bot started. Press Ctrl+C to exit.")
    await asyncio.idle()  # Keep the bot running
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())  # Use asyncio.run to run the main function
