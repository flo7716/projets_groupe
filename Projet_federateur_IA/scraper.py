import requests
from bs4 import BeautifulSoup
import spacy
import re
import boto3
from datetime import datetime
import xml.etree.ElementTree as ET

# Charger le modèle léger de SpaCy
nlp = spacy.load('en_core_web_sm')

# Modèle regex pour ignorer les sections non pertinentes
ignore_pattern = r"\bLatest AI|Amazon|Apps|Biotech & Health|Climate|Cloud Computing|Commerce|Crypto|Enterprise|EVs|Fintech|Fundraising|Gadgets|Gaming|Google|Government & Policy|Hardware|Instagram|Layoffs|Media & Entertainment|Meta|Microsoft|Privacy|Robotics|Security|Social|Space|Startups|TikTok|Transportation|Venture|Events|Startup Battlefield|StrictlyVC|Newsletters|Podcasts|Videos|Partner Content|TechCrunch Brand Studio|Crunchboard|Contact Us\b"

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Remplacer par la région de DynamoDB
table = dynamodb.Table('articles')  # Assure-toi que la table 'articles' existe

# Fonction pour récupérer les URLs des articles depuis le sitemap
def fetch_article_urls_from_sitemap(sitemap_url):
    try:
        # Ajouter un en-tête 'User-Agent' pour éviter d'être bloqué par des protections anti-bot
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parser le fichier XML du sitemap
        root = ET.fromstring(response.content)

        # Extraire les URLs des articles (ne prendre que celles qui commencent par /article/)
        article_urls = []
        for url in root.findall(".//url/loc"):
            article_url = url.text
            if article_url.startswith("https://www.computerworld.com/article/"):
                article_urls.append(article_url)

        return article_urls

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du sitemap: {e}")
        return []

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

        # Filtrer les sections non pertinentes avec `ignore_pattern`
        article_text = re.sub(ignore_pattern, '', article_text, flags=re.IGNORECASE)
        article_text = re.sub(r'\s+', ' ', article_text).strip()  # Nettoyage des espaces multiples

        # Utilisation de SpaCy pour générer un résumé ou une description de l'article
        summary = "Résumé non disponible"
        if article_text and len(article_text) > 100:  # Vérifier que le contenu est suffisant
            doc = nlp(article_text)
            sentences = [sent.text for sent in doc.sents]
            summary = ' '.join(sentences[:3]) if len(sentences) >= 3 else article_text[:200]  # Résumer les 3 premières phrases

        # Recherche de l'image
        image_tag = soup.find('meta', {'property': 'og:image'})
        image_url = image_tag['content'] if image_tag else 'Image non trouvée'

        # Formatage de la date pour correspondre à un format lisible
        try:
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d') if date != 'Date non trouvée' else date
        except ValueError:
            date = 'Date non trouvée'

        # Retourner les données extraites sous forme de dictionnaire
        return {
            'url': url,
            'title': title,
            'summary': summary,
            'datePublication': date,
            'image_url': image_url,
            'source': url,
            'journal_name': 'ComputerWorld',  # Nom du journal mis à jour
        }

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

# Fonction pour scraper et stocker les articles
def scrape_and_store_articles():
    sitemap_url = "https://www.computerworld.com/sitemap_index.xml"
    article_urls = fetch_article_urls_from_sitemap(sitemap_url)

    for url in article_urls:
        article = scrape_article(url)
        if article:
            add_article_to_dynamodb(article)  # Appel de la fonction d'ajout dans DynamoDB

# Lancer le script
if __name__ == "__main__":
    print("Démarrage du scraping et de l'ajout d'articles...")
    scrape_and_store_articles()
    print("Script terminé.")
