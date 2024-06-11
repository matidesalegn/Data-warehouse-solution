import pandas as pd
import re
import string
from collections import Counter
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
        self.keywords = Counter()

    def load_data(self):
        """Load the CSV file into a pandas DataFrame."""
        self.data = pd.read_csv(self.file_path)
        print("Data loaded successfully.")
        return self.data

    def clean_text(self):
        """Combine all messages and clean the text."""
        combined_text = ' '.join(self.data['message_text'].astype(str))
        # Remove URLs
        combined_text = re.sub(r'http\S+|www\S+|https\S+', '', combined_text, flags=re.MULTILINE)
        # Remove punctuation
        combined_text = combined_text.translate(str.maketrans('', '', string.punctuation))
        # Tokenize the text
        tokens = word_tokenize(combined_text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.lower() not in stop_words]
        # Join the cleaned tokens
        self.cleaned_text = ' '.join(tokens)
        print("Text cleaned successfully.")
        return self.cleaned_text

    # def extract_keywords(self, num_keywords=10):
    #     """Extract and count the most frequent words."""
    #     tokens = word_tokenize(self.cleaned_text)
    #     self.keywords = Counter(tokens)
    #     common_keywords = self.keywords.most_common(num_keywords)
    #     print("Keywords extracted successfully.")
    #     return common_keywords

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
    keywords = extractor.extract_keywords(num_keywords=10)
    print("Most common keywords:", keywords)