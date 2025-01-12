from flask import Flask, request, jsonify
import boto3
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

# Configurer DynamoDB pour deux tables
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Tables DynamoDB
articles_table = dynamodb.Table('articles')
associations_table = dynamodb.Table('assos')

# Récupérer tous les articles
@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        response = articles_table.scan()
        articles = response.get('Items', [])
        return jsonify({"message": "Articles récupérés avec succès!", "articles": articles}), 200
    except Exception as e:
        return jsonify({"message": "Erreur lors de la récupération des articles.", "error": str(e)}), 500

# Ajouter un article
@app.route('/api/articles', methods=['POST'])
def add_article():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"message": "Le titre et le contenu sont requis!"}), 400

    # Créer un article et l'ajouter à DynamoDB
    article_id = str(uuid4())
    created_at = datetime.now().isoformat()

    articles_table.put_item(
        Item={
            'id': article_id,
            'title': title,
            'content': content,
            'createdAt': created_at
        }
    )

    return jsonify({"message": "Article ajouté avec succès!", "article": data}), 201

# Récupérer toutes les associations
@app.route('/api/associations', methods=['GET'])
def get_associations():
    try:
        response = associations_table.scan()
        associations = response.get('Items', [])
        return jsonify({"message": "Associations récupérées avec succès!", "associations": associations}), 200
    except Exception as e:
        return jsonify({"message": "Erreur lors de la récupération des associations.", "error": str(e)}), 500

# Ajouter une association
@app.route('/api/associations', methods=['POST'])
def add_association():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({"message": "Le nom et la description sont requis!"}), 400

    # Créer une association et l'ajouter à DynamoDB
    association_id = str(uuid4())
    created_at = datetime.now().isoformat()

    associations_table.put_item(
        Item={
            'id': association_id,
            'name': name,
            'description': description,
            'createdAt': created_at
        }
    )

    return jsonify({"message": "Association ajoutée avec succès!", "association": data}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
