from flask import Flask, render_template, request, jsonify
import boto3

app = Flask(__name__)

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
table = dynamodb.Table('assos')

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher toutes les associations
@app.route('/assos', methods=['GET'])
def get_assos():
    try:
        response = table.scan()
        assos = response.get('Items', [])
        return jsonify(assos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour rechercher une association par mot-clé
@app.route('/search', methods=['GET'])
def search_assos():
    keyword = request.args.get('keyword', '').lower()
    try:
        response = table.scan()
        assos = response.get('Items', [])
        filtered_assos = [asso for asso in assos if keyword in asso['name'].lower()]
        return jsonify(filtered_assos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
