import pandas as pd
import re

def preprocess_amharic_text(text):
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters, keep Amharic characters (Unicode range for Amharic: U+1200–U+137F)
    text = re.sub(r'[^\u1200-\u137F\s\d\w]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

# Load raw data
try:
    df = pd.read_csv('data\\raw\\telegram_data.csv', encoding='utf-8')
except FileNotFoundError:
    print("Error: telegram_data.csv not found in data\\raw")
    exit()

# Preprocess text
df['cleaned_text'] = df['text'].apply(preprocess_amharic_text)

# Separate metadata
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time

# Save preprocessed data
df.to_csv('data\\processed\\preprocessed_data.csv', index=False, encoding='utf-8')
print("Preprocessed data saved to data\\processed\\preprocessed_data.csv")