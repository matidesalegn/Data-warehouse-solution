import os
import pytest
from telegram_scraper import scrape_telegram_channel

@pytest.fixture
def mock_telegram_api(mocker):
    # Mock the Telethon client
    mock_client = mocker.patch('telegram_scraper.TelegramClient')
    return mock_client

def test_scrape_telegram_channel(mock_telegram_api):
    mock_telegram_api.return_value.get_messages.return_value = [
        {'id': 1, 'message': 'Test message 1'},
        {'id': 2, 'message': 'Test message 2'}
    ]

    scrape_telegram_channel('test_channel')

    # Check if the data was saved correctly
    assert os.path.exists('raw_data/messages.csv')

    with open('raw_data/messages.csv', 'r') as file:
        content = file.read()
        assert 'Test message 1' in content
        assert 'Test message 2' in content