import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import time
import requests
import os

# Your Koyeb app's URL (or a health check endpoint if you have one)
KOYEB_APP_URL = ""


async def keep_alive():
    """Keeps the Koyeb app alive by sending periodic requests."""
    while True:
        try:
            response = requests.get(KOYEB_APP_URL)
            if response.status_code == 200:  # Adjust condition based on your health check response
                print("Keep-alive ping successful.")
            else:
                print(f"Keep-alive ping failed: Status code {response.status_code}")
        except Exception as e:
            print(f"Keep-alive ping error: {e}")
        await asyncio.sleep(60 * 15)  # Ping every 15 minutes.

def run_keep_alive():
    """Runs the keep-alive function in an asyncio event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(keep_alive())

if __name__ == "__main__":
    print("Bot starting...")
    # Start the keep-alive thread
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()

    # Run the bot
    print("Bot started.  Waiting for messages...")
    app.run()
