from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Load labeled data
tokens, labels = [], []
current_sentence = []
with open('data\\processed\\labeled_data.conll', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            token, label = line.strip().split()
            current_sentence.append((token, label))
        else:
            if current_sentence:
                t, l = zip(*current_sentence)
                tokens.append(list(t))
                labels.append(list(l))
            current_sentence = []

# Create dataset
data = {'tokens': tokens, 'ner_tags': labels}
dataset = Dataset.from_dict(data)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base')
model = AutoModelForTokenClassification.from_pretrained('xlm-roberta-base', num_labels=7)

# Tokenize dataset
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['tokens'], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples['ner_tags']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)
            else:
                label_ids.append(['O', 'B-Product', 'I-Product', 'B-Price', 'I-Price', 'B-Location', 'I-Location'].index(label[word_id]))
        labels.append(label_ids)
    tokenized_inputs['labels'] = labels
    return tokenized_inputs

tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir='models',
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=1,  # Minimal
    weight_decay=0.01,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Train
trainer.train()
model.save_pretrained('models\\ner_model')
tokenizer.save_pretrained('models\\ner_model')
print("Model saved to models\\ner_model")