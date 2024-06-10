import os
import csv
import logging
import logging.config
import yaml
import argparse
from telethon import TelegramClient
import uuid  # Import UUID for generating unique identifiers

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

# Channels to collect images from (specific channels)
image_channels = ['CheMed123', 'lobelia4cosmetics']

async def scrape_telegram_channels(min_id=None):
    all_messages = []
    for username in channel_usernames:
        async for message in client.iter_messages(username, min_id=min_id or 0):
            message_id = str(uuid.uuid4())  # Generate a unique identifier
            all_messages.append({
                'message_id': message_id,  # Store the unique identifier
                'sender_id': message.sender_id,
                'message_text': message.text,
                'channel': username
            })
            logger.info(f"Scraped message from {username}: {message.text}")
    return all_messages

async def scrape_images(min_id=None):
    for username in image_channels:
        if username in channel_usernames:
            async for message in client.iter_messages(username, min_id=min_id or 0):
                if message.photo:
                    # Generate a unique identifier for the image
                    message_id = str(uuid.uuid4())
                    # Save image with unique identifier and channel name as prefix
                    path = await message.download_media(file=f'raw_data/images/{username}_{message_id}.jpg')
                    logger.info(f"Downloaded image from {username}: {path}")

def store_data(messages, filepath='raw_data/messages.csv'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['message_id', 'sender_id', 'message_text', 'channel'])
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