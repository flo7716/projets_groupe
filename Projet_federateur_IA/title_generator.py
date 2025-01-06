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

if __name__ == "__main__":
    sample_text = "Some article content goes here..."
    title = extract_title_using_bert(sample_text)
    print(f"Titre extrait : {title}")
