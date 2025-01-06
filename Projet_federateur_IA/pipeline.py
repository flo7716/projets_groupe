import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pymysql
import os
from dotenv import load_dotenv
import spacy
from flask import Flask, jsonify

# Charger les variables d'environnement
load_dotenv()

# Liste des mots à ignorer pour le filtrage
IGNORE_LIST = [
    "Latest", "AI", "Amazon", "Apps", "Biotech & Health", "Climate", "Cloud Computing", 
    "Commerce", "Crypto", "Enterprise", "EVs", "Fintech", "Fundraising", "Gadgets", 
    "Gaming", "Google", "Government & Policy", "Hardware", "Instagram", "Layoffs", 
    "Media & Entertainment", "Meta", "Microsoft", "Privacy", "Robotics", "Security", 
    "Social", "Space", "Startups", "TikTok", "Transportation", "Venture", "Events", 
    "Startup Battlefield", "StrictlyVC", "Newsletters", "Podcasts", "Videos", 
    "Partner Content", "TechCrunch Brand Studio", "Crunchboard", "Contact Us"
]

# Charger le modèle Spacy (modèle anglais)
nlp = spacy.load("en_core_web_sm")

# 1. Extraction des liens d'articles depuis TechCrunch
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
        if len(article_links) >= 10:
            break

    return list(article_links)

# 2. Nettoyage du texte
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

# 3. Génération du titre à partir du texte avec Spacy
def extract_title_using_spacy(text):
    doc = nlp(text)
    # Prendre la première phrase comme titre
    title = " ".join([sent.text for sent in doc.sents][:1])
    return title

# 4. Filtrage du texte en fonction des termes à ignorer
def filter_summary(text):
    ignore_pattern = r"|".join(re.escape(phrase) for phrase in IGNORE_LIST)
    text = re.sub(ignore_pattern, '', text)
    return text.strip()

# 5. Sauvegarde dans la base de données MySQL
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

# API backend Flask pour récupérer les articles
app = Flask(__name__)

articles = []

@app.route('/api/articles', methods=['GET'])
def get_articles():
    return jsonify(articles)

# Fonction principale pour exécuter tout le flux
def main():
    base_url = 'https://techcrunch.com/'
    article_urls = extract_article_links(base_url)

    for article_url in article_urls:
        # Récupération de l'article
        article_response = requests.get(article_url)
        if article_response.status_code != 200:
            print(f"Erreur lors de la récupération de l'article {article_url}")
            continue

        soup = BeautifulSoup(article_response.content, 'html.parser')
        article_text = soup.get_text()
        
        # Nettoyage du texte
        cleaned_text = clean_text(article_text)

        # Génération du titre avec Spacy
        title = extract_title_using_spacy(cleaned_text)

        # Filtrage du résumé
        summary = filter_summary(cleaned_text)

        # Sauvegarde dans la base de données
        save_to_database(article_url, title, summary, article_text)

        # Ajouter à la liste d'articles pour l'API
        articles.append({
            "url": article_url,
            "title": title,
            "summary": summary
        })
    
    # Lancer l'API Flask
    app.run(debug=True, use_reloader=False)  # Désactive le reloader pour une meilleure gestion de la mémoire

if __name__ == '__main__':
    main()
