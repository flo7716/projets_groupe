import requests
from bs4 import BeautifulSoup
import spacy
import boto3
from datetime import datetime

# Chargement du modèle SpaCy (version légère)
nlp = spacy.load('en_core_web_sm')  # Utiliser le modèle léger pour éviter une surcharge mémoire

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Remplacer par la région de DynamoDB
table = dynamodb.Table('articles')  # Assure-toi que la table 'articles' existe

# Fonction pour scrapper un article
def scrape_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Si le statut HTTP est 4xx ou 5xx, cela soulève une exception

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraction des informations de l'article
        title = soup.find('h1') or soup.find('title')
        title = title.get_text() if title else 'Titre non trouvé'

        date = soup.find('time')  # Recherche de la balise <time>
        date = date.get_text() if date else 'Date non trouvée'

        # Extraire le contenu de l'article
        article_content = soup.find('div', {'class': 'article-body'})  # Classe spécifique à ajuster selon la structure du site
        article_content = article_content.get_text() if article_content else 'Contenu non trouvé'

        # Utilisation de SpaCy pour générer un résumé ou une description de l'article
        doc = nlp(article_content)
        summary = ' '.join([sent.text for sent in doc.sents][:3])  # Résumer les 3 premières phrases

        # Recherche de l'image et autres informations
        image_url = soup.find('meta', {'property': 'og:image'})  # Recherche de l'image partagée sur les réseaux sociaux
        image_url = image_url['content'] if image_url else 'Image non trouvée'

        # Formatage de la date pour correspondre à un format lisible
        try:
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d') if date != 'Date non trouvée' else date
        except ValueError:
            # Essayer d'autres formats ou laisser la date inchangée
            date = 'Date non trouvée'

        # Gestion des paywalls et articles inaccessibles
        if "paywall" in response.text.lower():
            return None  # Si l'article est derrière un paywall, retourner None

        # Retourner les données extraites sous forme de dictionnaire
        return {
        'url': url,
        'title': title,
        'summary': summary,
        'datePublication': date,
        'image_url': image_url,
        'source': f'TechCrunch: {url}',  # Utilisation du formatage de chaîne f-string
        }

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

# Fonction pour ajouter un article dans DynamoDB
def add_article_to_dynamodb(article_data):
    try:
        table.put_item(Item=article_data)
        print(f"Article ajouté dans DynamoDB: {article_data['title']}")
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'article dans DynamoDB: {e}")

# Fonction pour récupérer automatiquement les URLs des articles d'une page d'index
def get_article_urls_from_index(url, limit=5):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Si le statut HTTP est 4xx ou 5xx, cela soulève une exception

        soup = BeautifulSoup(response.content, 'html.parser')

        # Rechercher tous les liens d'articles dans la page d'index
        article_links = []

        # Exemple : pour TechCrunch, les liens sont souvent dans des balises <a> avec une classe spécifique
        for link in soup.find_all('a', {'href': True}):
            href = link['href']
            if 'techcrunch.com' in href and '/2025/' in href:  # Assurer de ne récupérer que les articles récents
                article_links.append(f"https://techcrunch.com{href}" if not href.startswith('http') else href)
            
            # Limiter à 5 articles
            if len(article_links) >= limit:
                break

        return article_links

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'index {url}: {e}")
        return []

# Fonction pour scrapper et stocker les articles
def scrape_and_store_articles():
    # URL de la page d'index (ex: page d'accueil ou une page d'articles récents)
    index_url = "https://techcrunch.com/"

    # Obtenir tous les liens d'articles de la page d'index, limité à 5
    article_urls = get_article_urls_from_index(index_url, limit=5)

    # Scraper chaque article et l'ajouter dans DynamoDB
    for url in article_urls:
        article = scrape_article(url)
        if article:
            add_article_to_dynamodb(article)

# Lancer le script
if __name__ == "__main__":
    scrape_and_store_articles()
