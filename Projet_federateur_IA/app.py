from flask import Flask, jsonify, request, render_template
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name="eu-west-3",
    aws_access_key_id="AKIAZPPF76IFIMCT6M6I",
    aws_secret_access_key="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"
)
table = dynamodb.Table('articles')  # Assure-toi que la table 'articles' existe

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/articles/<string:article_id>/detail', methods=['GET'])
def article_detail(article_id):
    try:
        print(f"Fetching article with ID: {article_id}")  # Debugging information
        response = table.get_item(Key={'article_id': article_id})  # Use the correct key name
        article = response.get('Item')
        if not article:
            print(f"Article with ID {article_id} not found")  # Debugging information
            return render_template('404.html'), 404
        print(f"Article found: {article}")  # Debugging information
        return render_template('article_detail.html', article=article)
    except Exception as e:
        print(f"Error fetching article: {str(e)}")  # Debugging information
        return render_template('500.html', error=str(e)), 500
    
    
@app.route('/articles/<string:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        response = table.delete_item(Key={'article_id': article_id})
        return jsonify({'message': 'Article deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')