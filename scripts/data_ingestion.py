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

# Define six Ethiopian e-commerce Telegram channels
channels = [
    '@Leyueqa',
    '@helloomarketethiopia',
    '@AwasMart',
    '@efuyegellaMarket',
    '@abaymart',
]

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start client with 2FA support
    await client.start(
        phone=phone_number,
        password=lambda: input("Please enter your 2FA password: ") if os.getenv('TELEGRAM_2FA_PASSWORD') else None
    )
    data = []

    for channel in channels:
        try:
            async for message in client.iter_messages(channel, limit=50):
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
    df.to_csv('data\\raw\\telegram_data.csv', index=False, encoding='utf-8-sig')
    print("Data saved to data\\raw\\telegram_data.csv")

with client:
    client.loop.run_until_complete(main())