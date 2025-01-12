from flask import Flask, jsonify
import boto3

# Initialiser Flask
app = Flask(__name__)

# Configurer DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Remplacer par la région de DynamoDB
table = dynamodb.Table('articles')

# Route pour récupérer la liste des associations
@app.route('/api/assos', methods=['GET'])
def get_associations():
    response = table.scan()  # Récupérer tous les éléments de la table
    articles = response.get('Items', [])
    return jsonify(articles)

# Route pour récupérer les détails d'une association
@app.route('/api/assos/<assoc_id>', methods=['GET'])
def get_association_details(assoc_id):
    response = table.get_item(Key={'assoc_id': assoc_id})
    article = response.get('Item', {})
    return jsonify(article)

if __name__ == '__main__':
    app.run(debug=True)
