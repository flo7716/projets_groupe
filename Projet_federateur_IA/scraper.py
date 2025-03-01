import requests
from bs4 import BeautifulSoup
import spacy
import re
import boto3
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

# Using spacy.load().
nlp = spacy.load("en_core_web_sm")

# Configuration DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
table = dynamodb.Table('articles')  # Assure-toi que la table 'articles' existe

# Fonction pour scrapper un article
def scrape_article(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Si le statut HTTP est 4xx ou 5xx, cela soulève une exception

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraction des informations de l'article
        title = soup.find('h1') or soup.find('title')
        title = title.get_text(strip=True) if title else 'Titre non trouvé'

        date = soup.find('time')  # Recherche de la balise <time>
        date = date.get_text(strip=True) if date else 'Date non trouvée'

        # Extraire le contenu de l'article
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text().strip() for para in paragraphs])
        article_text = clean_text(article_text)

        # Utilisation de SpaCy pour générer un résumé ou une description de l'article
        summary = "Résumé non disponible"
        if article_text and len(article_text) > 100:  # Vérifier que le contenu est suffisant
            doc = nlp(article_text)
            sentences = [sent.text for sent in doc.sents]
            summary = ' '.join(sentences[:10]) if len(sentences) >= 10 else article_text[:200]  # Résumer les 10 premières phrases

        # Recherche de l'image
        image_tag = soup.find('meta', {'property': 'og:image'})
        image_url = image_tag['content'] if image_tag else 'Image non trouvée'

        # Formatage de la date pour correspondre à un format lisible
        try:
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d') if date != 'Date non trouvée' else date
        except ValueError:
            date = 'Date non trouvée'

        # Générer un ID unique pour l'article en utilisant un hash de l'URL
        article_id = hashlib.md5(url.encode()).hexdigest()

        # Retourner les données extraites sous forme de dictionnaire
        article_data = {
            'article_id': article_id,
            'url': url,
            'title': title,
            'summary': summary,
            'datePublication': datetime.now().isoformat(),
            'image_url': image_url,
            'source': url,
            'journal_name': 'ComputerWorld',  # Nom du journal mis à jour
        }

        print(f"Article data: {article_data}")  # Debugging information
        return article_data

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

# Fonction pour ajouter un article dans DynamoDB
def add_article_to_dynamodb(article_data):
    try:
        table.put_item(Item=article_data)
        print(f"Article ajouté dans DynamoDB : {article_data['title']}")  # Affichage du titre de l'article ajouté
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'article dans DynamoDB: {e}")
        print(f"Article qui n'a pas pu être ajouté: {article_data}")

# Fonction pour récupérer automatiquement les URLs des articles d'une page d'index
def get_article_urls_from_index(url, limit=5):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Si le statut HTTP est 4xx ou 5xx, cela soulève une exception

        soup = BeautifulSoup(response.content, 'html.parser')

        # Rechercher tous les liens d'articles dans la page d'index
        article_links = set()

        for link in soup.find_all('a', {'href': True}):
            href = link['href']
            if 'computerworld.com' in href and '/article/' in href:
                article_links.add(f"https://www.computerworld.com{href}" if not href.startswith('http') else href)

            # Limiter à 5 articles
            if len(article_links) >= limit:
                break

        return list(article_links)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'index {url}: {e}")
        return []

# Fonction pour nettoyer le texte brut
def clean_text(text):
    """Nettoie le texte brut."""
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un espace unique
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Supprimer les caractères non-ASCII
    return text.strip()

# Fonction pour scraper et stocker les articles
def scrape_and_store_articles():
    index_url = "https://www.computerworld.com/"
    article_urls = get_article_urls_from_index(index_url, limit=5)

    for url in article_urls:
        article = scrape_article(url)
        if article:
            add_article_to_dynamodb(article)  # Appel de la fonction d'ajout dans DynamoDB

# Lancer le script
if __name__ == "__main__":
    print("Démarrage du scraping et de l'ajout d'articles...")
    scrape_and_store_articles()
    print("Script terminé.")
