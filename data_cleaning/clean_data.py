import pandas as pd
import os
import logging
import logging.config
import yaml

# Ensure necessary directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('cleaned_data', exist_ok=True)

# Load logging configuration
with open('logging_config.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def clean_data(input_filepath='../data_cleaning/filtered_medical_messages.csv', output_filepath='cleaned_data/messages_cleaned.csv'):
    # Read data
    try:
        df = pd.read_csv(input_filepath)
        logger.info(f"Loaded data from {input_filepath}")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    logger.info("Removed duplicates")

    # Handle missing values (e.g., drop rows with missing values)
    df.dropna(inplace=True)
    logger.info("Handled missing values")

    # Standardize formats (e.g., trim whitespace)
    df['message_text'] = df['message_text'].str.strip()
    logger.info("Standardized formats")

    # Data validation (e.g., ensure no empty messages)
    df = df[df['message_text'] != '']
    logger.info("Validated data")

    # Store cleaned data
    try:
        df.to_csv(output_filepath, index=False)
        logger.info(f"Stored cleaned data to {output_filepath}")
    except Exception as e:
        logger.error(f"Error storing cleaned data: {e}")

if __name__ == '__main__':
    clean_data()