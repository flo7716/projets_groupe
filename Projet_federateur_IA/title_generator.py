from transformers import BertTokenizer, TFBertForSequenceClassification
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

def extract_title_using_bert(text):
    inputs = tokenizer(text, return_tensors="tf", max_length=512, truncation=True, padding="max_length")
    outputs = model(inputs)
    logits = outputs.logits
    predicted_class = np.argmax(logits, axis=-1)
    title = "Titre prédictif basé sur le modèle BERT"
    return title

def generate_titles(cleaned_texts):
    titles = []
    for text in cleaned_texts:
        title = extract_title_using_bert(text)
        titles.append(title)
    return titles

if __name__ == "__main__":
    titles = generate_titles(["Some article content goes here..."])
    print(titles)
