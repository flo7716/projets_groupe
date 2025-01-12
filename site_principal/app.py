from flask import Flask, render_template, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialisation du client DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Remplace par la région AWS appropriée
table = dynamodb.Table('associations')  # Remplace par le nom de ta table DynamoDB

# Route pour la page d'accueil (liste des associations)
@app.route('/')
def home():
    try:
        # Récupérer toutes les associations depuis DynamoDB
        response = table.scan()
        associations = response['Items']
        return render_template('assos.html', associations=associations)
    except ClientError as e:
        return jsonify({"error": f"Erreur DynamoDB: {e.response['Error']['Message']}"})

# Route pour afficher les détails d'une association
@app.route('/association/<int:id>')
def details(id):
    try:
        # Récupérer une association spécifique par son ID
        response = table.get_item(Key={'id': id})
        if 'Item' in response:
            association = response['Item']
            return render_template('details.html', association=association)
        else:
            return jsonify({"error": "Association non trouvée"})
    except ClientError as e:
        return jsonify({"error": f"Erreur DynamoDB: {e.response['Error']['Message']}"})

# Route pour obtenir les données des associations au format JSON (API)
@app.route('/api/associations')
def api_associations():
    try:
        # Récupérer toutes les associations au format JSON
        response = table.scan()
        associations = response['Items']
        return jsonify(associations)
    except ClientError as e:
        return jsonify({"error": f"Erreur DynamoDB: {e.response['Error']['Message']}"})

if __name__ == '__main__':
    app.run(debug=True)
