from flask import Flask, render_template, request, jsonify
import boto3
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration DynamoDB avec les credentials chargées depuis .env
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
table = dynamodb.Table('articles')

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher tous les articles
@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        response = table.scan()
        articles = response.get('Items', [])
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour rechercher des articles par mot-clé
@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()
    try:
        response = table.scan()
        articles = response.get('Items', [])
        filtered_articles = [
            article for article in articles
            if keyword in article['title'].lower() or keyword in article['summary'].lower()
        ]
        return jsonify(filtered_articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour ajouter un nouvel article
@app.route('/add_article', methods=['POST'])
def add_article():
    data = request.json
    try:
        table.put_item(Item={
            'source': data['source'],
            'datePublication': data['datePublication'],
            'image_url': data['image_url'],
            'journal_name': data['journal_name'],
            'summary': data['summary'],
            'title': data['title'],
            'url': data['url']
        })
        return jsonify({"message": "Article added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    index()
