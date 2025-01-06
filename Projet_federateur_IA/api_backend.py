from flask import Flask, jsonify

app = Flask(__name__)

articles = [
    {"url": "https://techcrunch.com/article-1", "title": "Article 1", "summary": "Résumé de l'article 1"},
    {"url": "https://techcrunch.com/article-2", "title": "Article 2", "summary": "Résumé de l'article 2"},
]

@app.route('/api/articles', methods=['GET'])
def get_articles():
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
