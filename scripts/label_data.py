import pandas as pd
import re

def tokenize_and_label(text):
    if not isinstance(text, str):
        return []
    tokens = text.split()
    labels = []
    for token in tokens:
        if re.match(r'^\d+(\.\d+)?$', token):  # Price (e.g., 2800, 950)
            labels.append('B-Price')
        elif re.match(r'ብር$', token):  # Currency unit
            labels.append('I-Price')
        elif token in ['መጠጦች', 'ማቅረቢያ', 'ጫማ', 'ስልክ', 'ምንጣፍ', 'ማስጫ', 'ፍራሽ', 'ባትሪ', 'ማሞቂያ', 'ስቶቭ', 'ሲሊከን', 'ጁስ', 'ቡና', 'ቅመም', 'ትሬይ', 'መብራት']:  # Products from telegram_data.csv
            labels.append('B-Product')
        elif token in ['በአዲስ', 'መገናኛ', 'ፒያሳ', 'ልደታ', 'ባልቻ']:  # Locations
            labels.append('B-Location')
        elif token in ['አበባ', 'ሆስፒታል']:  # Location continuations
            labels.append('I-Location')
        else:
            labels.append('O')
    return list(zip(tokens, labels))

try:
    df = pd.read_csv('data\\processed\\preprocessed_data.csv', encoding='utf-8-sig')
except FileNotFoundError:
    print("Error: preprocessed_data.csv not found")
    exit()

labeled_data = []
for text in df['cleaned_text'].head(30):  # Label 30 messages
    labeled_data.extend(tokenize_and_label(text))

with open('data\\processed\\labeled_data.conll', 'w', encoding='utf-8') as f:
    for token, label in labeled_data:
        f.write(f"{token} {label}\n")
    f.write("\n")
print("Labeled data saved to data\\processed\\labeled_data.conll")