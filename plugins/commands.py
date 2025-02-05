
from pyrogram import Client, filters


# Define the admin's user ID (replace with your actual admin ID)
ADMIN_ID = 5356695781 # Replace this with your actual admin user ID

@Client.on_message(filters.command("id"))
def id_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"

    # Send the user ID to the user
    message.reply_text(f"Your User ID is: {user_id}")

    # Check if the user is the admin
    if user_id == ADMIN_ID:
        message.reply_text(f"Admin User ID is: {ADMIN_ID}")

    # Send the user ID to the admin as well
    client.send_message(ADMIN_ID, f"{user_name} (User ID: {user_id}) has requested their ID.")

if __name__ == "__main__":
    app = Client("my_bot")
