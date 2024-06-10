{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from telethon import TelegramClient, events\n",
    "import csv\n",
    "import sqlite3\n",
    "\n",
    "# Your API ID and hash from my.telegram.org\n",
    "api_id = 'YOUR_API_ID'\n",
    "api_hash = 'YOUR_API_HASH'\n",
    "\n",
    "# Create the client and connect\n",
    "client = TelegramClient('session_name', api_id, api_hash)\n",
    "\n",
    "async def main():\n",
    "    # Get information about yourself\n",
    "    me = await client.get_me()\n",
    "    print(me.stringify())\n",
    "\n",
    "    # Iterate over the specified channels and scrape data\n",
    "    channel_usernames = [\n",
    "        'DoctorsET', 'lobelia4cosmetics', 'yetenaweg', 'EAHCI'\n",
    "    ]\n",
    "\n",
    "    for username in channel_usernames:\n",
    "        async for message in client.iter_messages(username):\n",
    "            print(message.sender_id, message.text)\n",
    "\n",
    "with client:\n",
    "    client.loop.run_until_complete(main())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def store_data(messages):\n",
    "    with open('scraped_data.csv', mode='w') as file:\n",
    "        writer = csv.writer(file)\n",
    "        writer.writerow(['sender_id', 'message_text'])\n",
    "        for message in messages:\n",
    "            writer.writerow([message.sender_id, message.text])\n",
    "\n",
    "# Example usage:\n",
    "messages = []  # Assuming this list contains the scraped messages\n",
    "store_data(messages)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "conn = sqlite3.connect('scraped_data.db')\n",
    "c = conn.cursor()\n",
    "\n",
    "# Create table\n",
    "c.execute('''CREATE TABLE IF NOT EXISTS messages\n",
    "             (sender_id INTEGER, message_text TEXT)''')\n",
    "\n",
    "# Insert a row of data\n",
    "for message in messages:\n",
    "    c.execute(\"INSERT INTO messages (sender_id, message_text) VALUES (?, ?)\",\n",
    "              (message.sender_id, message.text))\n",
    "\n",
    "# Save (commit) the changes\n",
    "conn.commit()\n",
    "\n",
    "# Close the connection\n",
    "conn.close()"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
