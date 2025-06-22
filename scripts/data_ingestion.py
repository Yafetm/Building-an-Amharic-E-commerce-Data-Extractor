import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Define channels to scrape
channels = ['@animationsz']  # Replace with actual channel names

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    data = []

    for channel in channels:
        try:
            async for message in client.iter_messages(channel, limit=50):  # Reduced limit for interim submission
                if message.text or message.photo:
                    data.append({
                        'channel': channel,
                        'sender': message.sender_id,
                        'timestamp': message.date,
                        'text': message.text,
                        'has_image': bool(message.photo),
                        'message_id': message.id
                    })
        except Exception as e:
            print(f"Error scraping {channel}: {e}")

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data\\raw\\telegram_data.csv', index=False, encoding='utf-8')
    print("Data saved to data\\raw\\telegram_data.csv")

with client:
    client.loop.run_until_complete(main())