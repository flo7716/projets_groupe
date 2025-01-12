from flask import Flask, render_template, request, jsonify
import boto3

app = Flask(__name__)

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
table = dynamodb.Table('articles')

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher les articles
@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        response = table.scan()
        articles = response.get('Items', [])
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour rechercher un article par mot-clé
@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()
    try:
        response = table.scan()
        articles = response.get('Items', [])
        filtered_articles = [article for article in articles if keyword in article['summary'].lower()]
        return jsonify(filtered_articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
