import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class TelegramDataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.cleaned_text = ""
        self.medical_keywords = ["equipment", "medicine", "medical", "doctor", "hospital", "pharmacy", "surgery", "clinic", "health", "treatment"]

    def load_data(self):
        """Load the CSV file into a pandas DataFrame."""
        self.data = pd.read_csv(self.file_path)
        print("Data loaded successfully.")
        return self.data

    def clean_text(self):
        """Combine all messages and clean the text."""
        self.data['cleaned_text'] = self.data['message_text'].astype(str)
        # Remove URLs
        self.data['cleaned_text'] = self.data['cleaned_text'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+', '', x, flags=re.MULTILINE))
        # Remove punctuation
        self.data['cleaned_text'] = self.data['cleaned_text'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
        # Tokenize the text
        self.data['cleaned_text'] = self.data['cleaned_text'].apply(lambda x: word_tokenize(x))
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        self.data['cleaned_text'] = self.data['cleaned_text'].apply(lambda x: [word for word in x if word.lower() not in stop_words])
        # Join the cleaned tokens back into a string
        self.data['cleaned_text'] = self.data['cleaned_text'].apply(lambda x: ' '.join(x))
        print("Text cleaned successfully.")
        return self.data

    def filter_medical_keywords(self):
        """Filter and display messages related to the medical business."""
        medical_messages = self.data[self.data['cleaned_text'].str.contains('|'.join(self.medical_keywords), case=False, na=False)]
        print("Filtered medical-related messages:")
        print(medical_messages)
        return medical_messages

    def save_to_csv(self, dataframe, output_filepath='filtered_medical_messages.csv'):
        """Save the filtered medical-related messages to a CSV file."""
        dataframe.to_csv(output_filepath, index=False)
        print(f"Filtered medical messages saved to {output_filepath}")

    def display_data(self):
        """Display the first few rows of the dataframe."""
        if self.data is not None:
            print(self.data.head())
        else:
            print("Data not loaded yet.")

# Example usage
if __name__ == "__main__":
    file_path = '../data_collection/raw_data/messages.csv'
    extractor = TelegramDataExtractor(file_path)
    extractor.load_data()
    extractor.display_data()
    extractor.clean_text()
    medical_messages = extractor.filter_medical_keywords()
    extractor.save_to_csv(medical_messages, 'filtered_medical_messages.csv')
    print("Filtered medical messages:", medical_messages)