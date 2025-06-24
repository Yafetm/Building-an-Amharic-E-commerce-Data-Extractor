import pandas as pd
import re

def preprocess_amharic_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\u1200-\u137F\s\d\w]', '', text)
    return ' '.join(text.split())

try:
    df = pd.read_csv('data\\raw\\telegram_data.csv', encoding='utf-8')
except FileNotFoundError:
    print("Error: telegram_data.csv not found in data\\raw")
    exit()

df['cleaned_text'] = df['text'].apply(preprocess_amharic_text)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time
df.to_csv('data\\processed\\preprocessed_data.csv', index=False, encoding='utf-8-sig')
print("Preprocessed data saved to data\\processed\\preprocessed_data.csv")