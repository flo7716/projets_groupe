from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# Configuration DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Remplacer par la région de DynamoDB
table = dynamodb.Table('articles')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        # Récupérer tous les articles dans la table
        response = table.scan()
        articles = response.get('Items', [])
        return jsonify(articles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
