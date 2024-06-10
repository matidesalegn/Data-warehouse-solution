import logging

logging.basicConfig(filename='scraping.log', level=logging.INFO)

try:
    # Scraping logic here
    pass
except Exception as e:
    logging.error(f"Error occurred: {e}")