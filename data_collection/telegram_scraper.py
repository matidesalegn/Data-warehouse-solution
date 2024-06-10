from telethon import TelegramClient, events

# Your API ID and hash from my.telegram.org
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Get information about yourself
    me = await client.get_me()
    print(me.stringify())

    # Iterate over the specified channels and scrape data
    channel_usernames = [
        'DoctorsET', 'lobelia4cosmetics', 'yetenaweg', 'EAHCI'
    ]

    for username in channel_usernames:
        async for message in client.iter_messages(username):
            print(message.sender_id, message.text)

with client:
    client.loop.run_until_complete(main())