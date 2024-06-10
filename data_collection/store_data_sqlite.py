import sqlite3
import logging
import yaml

# Load logging configuration
with open('data_collection/logging_config.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    """ Create messages table """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        message_text TEXT NOT NULL
    );"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        logger.info("Created messages table")
    except sqlite3.Error as e:
        logger.error(f"Error creating table: {e}")

def store_data(conn, messages):
    """ Store messages in the SQLite database """
    sql = ''' INSERT INTO messages(sender_id, message_text)
              VALUES(?,?) '''
    cur = conn.cursor()
    for message in messages:
        cur.execute(sql, (message['sender_id'], message['message_text']))
    conn.commit()
    logger.info(f"Stored {len(messages)} messages in the database")

if __name__ == '__main__':
    database = 'data_collection/raw_data/messages.db'
    conn = create_connection(database)
    if conn:
        create_table(conn)
        # Assuming `messages` is obtained from telegram_scraper.py
        from telegram_scraper import scrape_telegram_channels, client
        with client:
            messages = client.loop.run_until_complete(scrape_telegram_channels())
            store_data(conn, messages)
        conn.close()
