
import asyncio
from pyrogram import Client, filters
import requests
import os

# Your Koyeb app's URL (or a health check endpoint if you have one)
KOYEB_APP_URL = "revolutionary-cammy-royalyashh-2b28d450.koyeb.app"



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

if __name__ == "__main__":
    print("Bot starting...")
    
    # Start the keep-alive task
    loop = asyncio.get_event_loop()
    loop.create_task(keep_alive())

    # Run the bot
    print("Bot started. Waiting for messages...")
    app.run()
