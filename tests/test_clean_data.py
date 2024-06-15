import pandas as pd
from clean_data import clean_raw_data

def test_clean_raw_data():
    raw_data = pd.DataFrame({
        'id': [1, 2, 3],
        'message': ['Test message 1', None, 'Test message 3']
    })

    cleaned_data = clean_raw_data(raw_data)

    # Check if the data was cleaned correctly
    assert len(cleaned_data) == 2
    assert cleaned_data['message'].isnull().sum() == 0
    assert 'Test message 1' in cleaned_data['message'].values
    assert 'Test message 3' in cleaned_data['message'].values