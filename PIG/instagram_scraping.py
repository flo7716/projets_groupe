from flask import Flask, request, jsonify
import mysql.connector
import requests
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
import csv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Clé API Apify
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_RUN_SYNC_URL = f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs/last/dataset/items?token={APIFY_API_TOKEN}"

# Chemin absolu pour le fichier CSV
CSV_PATH = os.getenv("CSV_PATH")

# Fonction pour se connecter à la base de données MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connecté à la base de données.")
        return connection
    except mysql.connector.Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None


def read_associations_from_csv(csv_path):
    associations = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    nom_asso = row[0]
                    account_name = row[1]
                    associations.append((nom_asso, account_name))
        print("Associations lues depuis le CSV.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
    return associations


# Vérifier si un post existe déjà
def post_exists(connection, short_code):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM EVENEMENT_ORGANISE_PAR_ASSO WHERE shortCode = %s"
        cursor.execute(query, (short_code,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as e:
        print(f"Erreur lors de la vérification du post : {e}")
        return False

# Insérer un événement
def insert_event(connection, nom_asso, short_code, description):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO EVENEMENT_ORGANISE_PAR_ASSO (shortCode, nomAsso, descriptionEvent)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (short_code, nom_asso, description))
        connection.commit()
        print(f"Événement {short_code} ajouté avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de l'insertion de l'événement : {e}")

# Insérer une association si nécessaire
def insert_association_if_not_exists(connection, nom_asso, domaine_asso):
    try:
        cursor = connection.cursor()
        query_check = "SELECT COUNT(*) FROM ASSOCIATION WHERE nomAsso = %s"
        cursor.execute(query_check, (nom_asso,))
        result = cursor.fetchone()
        if result[0] == 0:
            query_insert = "INSERT INTO ASSOCIATION (nomAsso, domaineAsso) VALUES (%s, %s)"
            cursor.execute(query_insert, (nom_asso, domaine_asso))
            connection.commit()
            print(f"Association {nom_asso} ajoutée avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de l'insertion de l'association : {e}")

# Fonction pour démarrer l'exécution de l'acteur Apify
def start_apify_actor(account_name):
    payload = {
        "directUrls": [f"https://www.instagram.com/{account_name}/"],
        "resultsLimit": 10
    }
    response = requests.post(f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs?token={APIFY_API_TOKEN}", json=payload)
    if response.status_code == 201:
        run_id = response.json()["data"]["id"]
        print(f"Acteur lancé avec succès, ID d'exécution : {run_id}")
        return run_id
    else:
        print(f"Erreur lors du lancement de l'acteur : {response.status_code} - {response.text}")
        return None

# Fonction pour récupérer les résultats de l'exécution de l'acteur
def get_apify_results(run_id):
    attempt = 0
    while attempt < 10:  # Limiter le nombre d'essais pour éviter une boucle infinie
        attempt += 1
        time.sleep(10)  # Attendre 10 secondes avant de vérifier les résultats
        response = requests.get(f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs/{run_id}/dataset/items?token={APIFY_API_TOKEN}")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Tentative {attempt}: Résultats non disponibles, réessayer...")
        else:
            print(f"Erreur lors de la récupération des résultats (Code {response.status_code}): {response.text}")
            break
    return None


@app.route("/scrape", methods=["POST"])
def scrape_account():
    # Lire les associations depuis le CSV
    associations = read_associations_from_csv(CSV_PATH)

    # Pour chaque association, démarrer le scraping
    results = []
    for nom_asso, account_name in associations:
        # Vous pouvez ici réutiliser le reste de votre logique pour chaque association
        db_connection = connect_to_db()
        if not db_connection:
            return jsonify({"error": "Impossible de se connecter à la base de données."}), 500

        try:
            insert_association_if_not_exists(db_connection, nom_asso, "domaine_asso")  # Ajouter le domaine si nécessaire

            # Démarrer l'acteur Apify pour obtenir les posts Instagram
            run_id = start_apify_actor(account_name)
            if not run_id:
                return jsonify({"error": f"Échec du lancement de l'acteur Apify pour {account_name}."}), 500

            # Récupérer les résultats du scraping
            scraped_data = get_apify_results(run_id)
            if not scraped_data:
                return jsonify({"error": "Échec de la récupération des résultats du scraping."}), 500

            # Filtrer et insérer les événements dans la base de données (logique déjà définie)
            days_limit = datetime.now() - timedelta(days=90)
            for post in scraped_data.get('items', []):
                short_code = post["shortCode"]
                post_date = datetime.strptime(post.get("timestamp", "").split("T")[0], "%Y-%m-%d")
                description = post.get("caption", "Pas de description.")
                if post_date < days_limit:
                    continue
                if post_exists(db_connection, short_code):
                    continue
                insert_event(db_connection, nom_asso, short_code, description)

            results.append(f"Scraping pour {account_name} terminé avec succès.")

        except Exception as e:
            results.append(f"Erreur avec {account_name}: {str(e)}")
        finally:
            db_connection.close()

    return jsonify({"message": "Scraping terminé", "details": results})

# Lancer Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
