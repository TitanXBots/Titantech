
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

app = Client("my_bot")  # Replace "my_bot" with your bot's name

# Command to start the link generation process
@Client.on_message(filters.command("flink") & filters.private)
async def flink_command(client, message):
    # Check if user is admin (implement your own admin check)
    if not is_admin(message.from_user.id):
        await message.reply("You do not have permission to use this command.")
        return

    # Show options for setting and starting the link generation process
    keyboard = [
        [InlineKeyboardButton("• sᴇᴛ ғᴏʀᴍᴀᴛ •", callback_data="set_format")],
        [InlineKeyboardButton("• sᴛᴀʀᴛ ᴘʀᴏᴄᴇss •", callback_data="start_process")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply("Choose an action:", reply_markup=reply_markup)

# Callback handler for button actions
@Client.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    if callback_query.data == "set_format":
        await callback_query.message.reply("Please send the link format (e.g., 360P = 2, 480P = 2).")
        await client.listen(callback_query.from_user.id, lambda m: format_handler(client, m, callback_query.from_user.id))

    elif callback_query.data == "start_process":
        await callback_query.message.reply("Please send the post link from the database channel.")
        await client.listen(callback_query.from_user.id, lambda m: start_process_handler(client, m, callback_query.from_user.id))

    elif callback_query.data == "refresh":
        await callback_query.message.reply("Status refreshed.")

async def format_handler(client, message, user_id):
    # Process the format input
    format_string = message.text
    # Here you can add code to validate and store the format
    await message.reply(f"Format set: {format_string}")

async def start_process_handler(client, message, user_id):
    # Process the post link
    post_link = message.text
    # Here you can add code to generate formatted links based on the stored format
    await message.reply(f"Generating links for: {post_link}")

def is_admin(user_id):
    # Implement your own logic to check if the user is an admin
    # For example, check against a list of admin user IDs
    admin_ids = [5356695781]  # Replace with your admin user IDs
    return user_id in admin_ids

# Start the bot
app.run()
