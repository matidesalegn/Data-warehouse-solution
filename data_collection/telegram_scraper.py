import os
import csv
import logging
import logging.config
import yaml
import argparse
from telethon import TelegramClient

# Ensure necessary directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('raw_data/images', exist_ok=True)

# Load logging configuration
with open('logging_config.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# Telegram API credentials
api_id = '28036061'
api_hash = '2400c765921b76f7cd50658053f0639b'
phone = '+251974619952'

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Argument parser setup
parser = argparse.ArgumentParser(description="Telegram Scraper")
parser.add_argument('--telegram-channel', type=str, help='Telegram channel to download data from')
parser.add_argument('--batch-file', type=str, help='File containing a list of Telegram channels')
parser.add_argument('--min-id', type=int, help='Offset ID for incremental updates')
args = parser.parse_args()

# Function to read channels from batch file
def read_channels_from_file(filepath):
    with open(filepath, 'r') as file:
        channels = [line.strip() for line in file if line.strip()]
    return channels

# Determine channels to scrape
if args.telegram_channel:
    channel_usernames = [args.telegram_channel]
elif args.batch_file:
    channel_usernames = read_channels_from_file(args.batch_file)
else:
    logger.error("No Telegram channel or batch file provided")
    exit(1)

# Channels to collect images from (as an example, using the same channels)
image_channels = channel_usernames

async def scrape_telegram_channels(min_id=None):
    all_messages = []
    for username in channel_usernames:
        async for message in client.iter_messages(username, min_id=min_id):
            all_messages.append({
                'sender_id': message.sender_id,
                'message_text': message.text
            })
            logger.info(f"Scraped message from {username}: {message.text}")
    return all_messages

async def scrape_images(min_id=None):
    for username in image_channels:
        async for message in client.iter_messages(username, min_id=min_id):
            if message.photo:
                path = await message.download_media(file='raw_data/images/')
                logger.info(f"Downloaded image from {username}: {path}")

def store_data(messages, filepath='raw_data/messages.csv'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['sender_id', 'message_text'])
        writer.writeheader()
        for message in messages:
            writer.writerow(message)
    logger.info(f"Stored {len(messages)} messages to {filepath}")

async def main():
    await client.start(phone)
    messages = await scrape_telegram_channels(min_id=args.min_id)
    store_data(messages)
    await scrape_images(min_id=args.min_id)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())