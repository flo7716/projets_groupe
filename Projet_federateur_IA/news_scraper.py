import requests
from bs4 import BeautifulSoup
import pymysql
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import numpy as np
from nltk.tokenize import sent_tokenize
from urllib.parse import urljoin
from flask import Flask, jsonify, request
import re
from dotenv import load_dotenv
import os

# Initialisation de Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur la page d'accueil de l'API!"


# Initialisation du modèle BERT et du tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')


# Liste des mots/phrases à supprimer
IGNORE_LIST = [
    "Latest", "AI", "Amazon", "Apps", "Biotech & Health", "Climate", "Cloud Computing", 
    "Commerce", "Crypto", "Enterprise", "EVs", "Fintech", "Fundraising", "Gadgets", 
    "Gaming", "Google", "Government & Policy", "Hardware", "Instagram", "Layoffs", 
    "Media & Entertainment", "Meta", "Microsoft", "Privacy", "Robotics", "Security", 
    "Social", "Space", "Startups", "TikTok", "Transportation", "Venture", "Events", 
    "Startup Battlefield", "StrictlyVC", "Newsletters", "Podcasts", "Videos", 
    "Partner Content", "TechCrunch Brand Studio", "Crunchboard", "Contact Us"
]

# Fonction pour récupérer tous les liens d'articles d'une page donnée
def extract_article_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    article_links = set()  # Utiliser un set pour éviter les doublons
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        full_link = urljoin(url, link)  # Compléter l'URL si nécessaire
        if 'techcrunch.com' in full_link and '/2025/' in full_link:
            article_links.add(full_link)

    return list(article_links)

# Fonction pour extraire et traiter le contenu d'un article
def scrape_single_article(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Récupérer le contenu de l'article (supposons qu'il soit dans des <p> ou autres)
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text().replace('\n', ' ').strip() for para in paragraphs])

        # Nettoyer le texte pour supprimer les retours à la ligne, espaces multiples, etc.
        article_text = clean_text(article_text)

        # Filtrer les résumés pour enlever l'enchaînement spécifique sans tout éliminer
        article_text = filter_summary(article_text)

        # Générer un résumé simple (par exemple, les 3 premières phrases)
        sentences = sent_tokenize(article_text)
        sentences = [sentence.replace('\n', ' ').strip() for sentence in sentences]
        summary = ' '.join(sentences[:3])  # Prendre les 3 premières phrases comme résumé

        # Utiliser BERT pour extraire un titre ou des informations
        title = extract_title_using_bert(article_text)
        
        # Sauvegarder l'article, le titre et le résumé dans la base de données
        save_to_database(url, title, summary, article_text)
        return {"url": url, "title": title, "summary": summary}
    else:
        return {"error": f"Échec de la récupération de l'article. Code statut : {response.status_code}"}

# Fonction pour extraire le titre avec BERT
def extract_title_using_bert(text):
    inputs = tokenizer(text, return_tensors="tf", max_length=512, truncation=True, padding="max_length")
    with tf.GradientTape() as tape:
        outputs = model(inputs)
        logits = outputs.logits
    predicted_class = np.argmax(logits, axis=-1)
    title = "Titre prédictif basé sur le modèle BERT"
    return title

# Fonction pour insérer l'article dans la base de données MySQL
def save_to_database(url, title, summary, article_text):
    connection = None
    cursor = None
    try:
        load_dotenv()

        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'your_password'),
            database=os.getenv('DB_NAME', 'news_db')
        )
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO articles (link, title, summary, content) 
            VALUES (%s, %s, %s, %s)
        """, (url, title, summary, article_text))

        connection.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fonction de nettoyage du texte
def clean_text(text):
    # Suppression des retours à la ligne, des espaces multiples, des caractères spéciaux inutiles
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'\n+', ' ', text)  # Remplacer les sauts de ligne par un espace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Supprimer les caractères non-ASCII
    text = text.strip()  # Supprimer les espaces au début et à la fin
    return text

# Fonction pour filtrer l'enchaînement spécifique sans tout éliminer
def filter_summary(text):
    # Ignore l'enchaînement "Latest AI Amazon Apps Biotech..." dans le texte
    ignore_pattern = r"\bLatest AI Amazon Apps Biotech & Health Climate Cloud Computing Commerce Crypto Enterprise EVs Fintech Fundraising Gadgets Gaming Google Government & Policy Hardware Instagram Layoffs Media & Entertainment Meta Microsoft Privacy Robotics Security Social Space Startups TikTok Transportation Venture Events Startup Battlefield StrictlyVC Newsletters Podcasts Videos Partner Content TechCrunch Brand Studio Crunchboard Contact Us\b"
    text = re.sub(ignore_pattern, '', text)  # Supprimer l'enchaînement spécifique

    # Nettoyer de nouveau après suppression
    text = clean_text(text)
    return text

# Route pour récupérer les articles
@app.route('/articles', methods=['GET'])
def get_articles():
    base_url = request.args.get('url', 'https://techcrunch.com/')
    article_urls = extract_article_links(base_url)
    
    if article_urls:
        articles = []
        for url in article_urls:
            articles.append(scrape_single_article(url))
        return jsonify(articles)
    else:
        return jsonify({"message": "Aucun article trouvé."})

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
