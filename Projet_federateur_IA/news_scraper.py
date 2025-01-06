import requests
from bs4 import BeautifulSoup
import pymysql
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import tensorflow as tf
import numpy as np
from nltk.tokenize import sent_tokenize
from urllib.parse import urljoin
from flask import Flask, jsonify, request
import re
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation de Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur la page d'accueil de l'API!"

# Initialisation du modèle DistilBERT et du tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

# Liste des mots/phrases à ignorer
IGNORE_LIST = [
    "Latest", "AI", "Amazon", "Apps", "Biotech & Health", "Climate", "Cloud Computing", 
    "Commerce", "Crypto", "Enterprise", "EVs", "Fintech", "Fundraising", "Gadgets", 
    "Gaming", "Google", "Government & Policy", "Hardware", "Instagram", "Layoffs", 
    "Media & Entertainment", "Meta", "Microsoft", "Privacy", "Robotics", "Security", 
    "Social", "Space", "Startups", "TikTok", "Transportation", "Venture", "Events", 
    "Startup Battlefield", "StrictlyVC", "Newsletters", "Podcasts", "Videos", 
    "Partner Content", "TechCrunch Brand Studio", "Crunchboard", "Contact Us"
]

# Fonction pour récupérer les liens d'articles d'une page donnée
def extract_article_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        full_url = urljoin(url, link)
        article_links.add(full_url)
        if len(article_links) >= 10:  # Limiter à 10 articles
            break

    return list(article_links)

# Fonction pour extraire et traiter le contenu d'un article
def scrape_single_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text().replace('\n', ' ').strip() for para in paragraphs])

        # Nettoyage du texte
        article_text = clean_text(article_text)

        # Filtrage des contenus indésirables
        article_text = filter_summary(article_text)

        # Génération d'un résumé simple
        sentences = sent_tokenize(article_text)
        sentences = [sentence.replace('\n', ' ').strip() for sentence in sentences]
        summary = ' '.join(sentences[:3])

        # Extraction du titre avec DistilBERT
        title = extract_title_using_distilbert(article_text)

        # Sauvegarde dans la base de données
        save_to_database(url, title, summary, article_text)
        return {"url": url, "title": title, "summary": summary}
    else:
        return {"error": f"Échec de la récupération de l'article. Code statut : {response.status_code}"}

# Fonction pour extraire un titre avec DistilBERT
def extract_title_using_distilbert(text):
    inputs = tokenizer(text, return_tensors="tf", max_length=512, truncation=True, padding="max_length")
    outputs = model(inputs)
    logits = outputs.logits
    predicted_class = np.argmax(logits, axis=-1)
    title = "Titre prédictif basé sur le modèle DistilBERT"
    return title

# Fonction pour insérer un article dans la base de données MySQL
def save_to_database(url, title, summary, article_text):
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
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
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'\n+', ' ', text)  # Remplacer les sauts de ligne par un espace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Supprimer les caractères non-ASCII
    text = text.strip()
    return text

# Fonction pour filtrer les contenus indésirables
def filter_summary(text):
    ignore_pattern = r"|".join(re.escape(phrase) for phrase in IGNORE_LIST)
    text = re.sub(ignore_pattern, '', text)
    return clean_text(text)

# Route pour récupérer les articles
@app.route('/articles', methods=['GET'])
def get_articles():
    base_url = request.args.get('url', 'https://techcrunch.com/')
    article_urls = extract_article_links(base_url)

    if article_urls:
        articles = []
        for url in article_urls[:10]:
            articles.append(scrape_single_article(url))
        return jsonify(articles)
    else:
        return jsonify({"message": "Aucun article trouvé."})

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
