import boto3
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# Charger le modèle SpaCy
nlp = spacy.load('en_core_web_sm')

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
table = dynamodb.Table('articles')

# Fonction pour extraire tous les articles
def fetch_articles():
    try:
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")
        return []

# Fonction pour analyser les mots-clés
def analyze_keywords(articles):
    all_keywords = []
    for article in articles:
        doc = nlp(article['summary'])
        keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
        all_keywords.extend(keywords)
    return Counter(all_keywords)

# Générer un nuage de mots
def generate_wordcloud(keyword_counts):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keyword_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Nuage de mots-clés")
    plt.show()

# Lancer l'analyse
if __name__ == "__main__":
    print("Récupération des articles...")
    articles = fetch_articles()

    if articles:
        print("Analyse des mots-clés...")
        keyword_counts = analyze_keywords(articles)
        print("Génération du nuage de mots...")
        generate_wordcloud(keyword_counts)
    else:
        print("Aucun article trouvé.")
