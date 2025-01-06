import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    raw_text = "Some raw text\n with unwanted characters!"
    cleaned_text = clean_text(raw_text)
    print(f"Texte nettoyé : {cleaned_text}")
