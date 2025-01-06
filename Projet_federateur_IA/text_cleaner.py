import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def clean_article_texts(article_urls):
    cleaned_texts = []
    for url in article_urls:
        # Supposons que l'on récupère l'article par son URL ici.
        # Pour la démonstration, on imagine que l'article est un texte simple.
        raw_text = "Some raw text for " + url  # Ceci doit être remplacé par la récupération réelle de l'article.
        cleaned_text = clean_text(raw_text)
        cleaned_texts.append(cleaned_text)
    return cleaned_texts

if __name__ == "__main__":
    cleaned_texts = clean_article_texts(["https://techcrunch.com/article-1", "https://techcrunch.com/article-2"])
    print(cleaned_texts)
