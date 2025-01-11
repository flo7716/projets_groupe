from flask import Flask, render_template, jsonify
import sys
import os

# Ajouter le chemin du projet fédérateur IA à sys.path pour pouvoir l'importer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Projet_federateur_IA')))

from scraper import scrape_articles  # Importer le script de scraping depuis 'Projet_federateur_IA'

app = Flask(__name__)

@app.route('/')
def home():
    # Page d'accueil
    return render_template('index.html')

@app.route('/articles')
def articles():
    # Retourner les articles sous forme de JSON (récupérés par scraping depuis Projet_federateur_IA)
    articles = scrape_articles()  # Appel de la fonction de scraping importée
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
