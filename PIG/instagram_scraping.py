from flask import Flask, request, jsonify
import mysql.connector
import requests
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "your_password",  # Remplacer par le mot de passe correct
    "database": "assos"
}

# Clé API Apify
APIFY_API_TOKEN = "apify_api_Lp2selhpX7ioHI35PkQPscJtMW3Anr3S0nvU"
APIFY_RUN_SYNC_URL = f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs/last/dataset/items?token={APIFY_API_TOKEN}"

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


# Endpoint pour scraper
@app.route("/scrape", methods=["POST"])
def scrape_account():
    data = request.json
    account_name = data.get("account_name")
    nom_asso = data.get("nom_asso")
    domaine_asso = data.get("domaine_asso")
    
    if not all([account_name, nom_asso, domaine_asso]):
        return jsonify({"error": "Les paramètres account_name, nom_asso et domaine_asso sont requis."}), 400

    db_connection = connect_to_db()
    if not db_connection:
        return jsonify({"error": "Impossible de se connecter à la base de données."}), 500

    try:
        insert_association_if_not_exists(db_connection, nom_asso, domaine_asso)

        # Démarrer l'acteur Apify pour obtenir les posts Instagram
        run_id = start_apify_actor(account_name)
        if not run_id:
            return jsonify({"error": "Échec du lancement de l'acteur Apify."}), 500

        # Récupérer les résultats du scraping
        scraped_data = get_apify_results(run_id)
        if not scraped_data:
            return jsonify({"error": "Échec de la récupération des résultats du scraping."}), 500

        # Filtrer les événements plus récents que 90 jours
        days_limit = datetime.now() - timedelta(days=90)
        for post in scraped_data.get('items', []):
            short_code = post["shortCode"]
            post_date = datetime.strptime(post.get("timestamp", "").split("T")[0], "%Y-%m-%d")
            description = post.get("caption", "Pas de description.")

            # Si la date du post est plus ancienne que le seuil limite, on ignore ce post
            if post_date < days_limit:
                continue
            # Vérifier si le post existe déjà dans la base de données
            if post_exists(db_connection, short_code):
                continue

            # Insérer le nouvel événement dans la base de données
            insert_event(db_connection, nom_asso, short_code, description)

        return jsonify({"message": f"Scraping pour {account_name} terminé avec succès."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db_connection.close()

# Lancer Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
