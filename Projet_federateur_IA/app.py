from flask import Flask, jsonify, request
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
table = dynamodb.Table('articles')  # Assure-toi que la table 'articles' existe

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        response = table.scan()
        articles = response.get('Items', [])
        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/articles', methods=['POST'])
def add_article():
    try:
        article_data = request.json
        table.put_item(Item=article_data)
        return jsonify({'message': 'Article added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/articles/<string:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        response = table.get_item(Key={'article_id': article_id})
        article = response.get('Item')
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        return jsonify(article)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/articles/<string:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        response = table.delete_item(Key={'article_id': article_id})
        return jsonify({'message': 'Article deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)