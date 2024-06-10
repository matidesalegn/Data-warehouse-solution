import csv
import logging
import yaml
from telethon import TelegramClient

# Load logging configuration
with open('logging_config.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# Telegram API credentials (replace with your own credentials)
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Telegram channels to scrape
channel_usernames = [
    'DoctorsET', 'lobelia4cosmetics', 'yetenaweg', 'EAHCI'
]

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def scrape_telegram_channels():
    all_messages = []
    for username in channel_usernames:
        async for message in client.iter_messages(username, limit=100):
            all_messages.append({
                'sender_id': message.sender_id,
                'message_text': message.text
            })
            logger.info(f"Scraped message from {username}: {message.text}")
    return all_messages

def store_data(messages, filepath='raw_data/messages.csv'):
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['sender_id', 'message_text'])
        writer.writeheader()
        for message in messages:
            writer.writerow(message)
    logger.info(f"Stored {len(messages)} messages to {filepath}")

async def main():
    await client.start()
    messages = await scrape_telegram_channels()
    store_data(messages)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())