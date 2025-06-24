from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained('models\\ner_model')
model = AutoModelForTokenClassification.from_pretrained('models\\ner_model')
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy='simple')

df = pd.read_csv('data\\processed\\preprocessed_data.csv', encoding='utf-8-sig')
test_texts = df['cleaned_text'].head(5).tolist()

with open('data\\processed\\evaluation_results.txt', 'w', encoding='utf-8') as f:
    for text in test_texts:
        if isinstance(text, str):
            predictions = nlp(text)
            f.write(f"Text: {text}\nPredictions: {predictions}\n\n")
print("Evaluation results saved to data\\processed\\evaluation_results.txt")