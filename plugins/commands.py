   import logging
   from pyrogram import Client, filters

ADMIN_ID = [5356695781]

   logging.basicConfig(level=logging.INFO)  # Or logging.DEBUG for more detailed logs

   # ... rest of your code ...

   @Client.on_message(filters.command("id"))
   def id_command(client, message):
       logging.info(f"Received /id command from user: {message.from_user.id}")  # Log who sent the command
       try:
           user_id = message.from_user.id
           user_name = message.from_user.first_name or "User"

           # Send the user ID to the user
           message.reply_text(f"Your User ID is: {user_id}")

           # Send the user ID to the admin as well
           client.send_message(ADMIN_ID, f"{user_name} (User ID: {user_id}) has requested their ID.")

           # Check if the user is the admin (do this AFTER sending the initial message)
           if user_id == ADMIN_ID:
               message.reply_text(f"You are the admin! Admin User ID is: {ADMIN_ID}")
       except Exception as e:
           logging.error(f"Error processing /id command: {e}") # Log any errors
           message.reply_text("An error occurred. Please try again later.") # Tell the user something went wrong

   if __name__ == "__main__":
       app.run()
