from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import connect, Error
from apify_client import ApifyClient

# Initialisation de Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur la page d'accueil de l'API!"

# Configuration de la base de données
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "your_password",
    "database": "assos"
}

# Clé API Apify
APIFY_API_KEY = "apify_api_Lp2selhpX7ioHI35PkQPscJtMW3Anr3S0nvU"

# Connexion à la base de données
def connect_to_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connecté à la base de données.")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

# Insérer un événement dans la base
def insert_event(connection, table, data):
    try:
        cursor = connection.cursor()
        query = f"""
        INSERT INTO {table} (id{table[:-1]}, idEvent, dateEvent, lieuEvent, descriptionEvent)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        connection.commit()
        print(f"Événement {data[1]} ajouté dans {table}.")
    except Error as e:
        print(f"Erreur lors de l'insertion de l'événement : {e}")

# Fonction pour lancer le scraping via Apify
def scrape_with_apify(account_name):
    client = ApifyClient(APIFY_API_KEY)
    run = client.actor("zuzka/instagram-scraper").call(
        run_input={"search": [account_name], "resultsLimit": 5}
    )
    return client.dataset(run["defaultDatasetId"]).list_items()

# Endpoint Flask pour scraper un compte Instagram
@app.route("/scrape", methods=["POST"])
def scrape_account():
    data = request.json
    account_name = data.get("account_name")
    instagram_link = data.get("instagram_link")
    
    if not account_name or not instagram_link:
        return jsonify({"error": "account_name et instagram_link sont requis."}), 400

    # Connexion à la base de données
    db_connection = connect_to_db()
    if not db_connection:
        return jsonify({"error": "Impossible de se connecter à la base de données."}), 500

    try:
        # Lancer le scraping
        scraped_data = scrape_with_apify(account_name)

        for post in scraped_data["items"]:
            event_id = post["shortCode"]
            event_date = post.get("timestamp", "").split("T")[0]
            description = post.get("caption", "Pas de description.")
            location = post.get("locationName", "Lieu non spécifié")

            table = "EVENEMENT_ORGANISE_PAR_ASSO" if "asso" in description.lower() else "EVENEMENT_ORGANISE_PAR_ENTREPRISE"
            organizer_id = "ID_ASSO_EXAMPLE" if "asso" in description.lower() else "ID_ENTREPRISE_EXAMPLE"

            event_data = (organizer_id, event_id, event_date, location, description)
            insert_event(db_connection, table, event_data)

        return jsonify({"message": f"Scraping pour {account_name} terminé avec succès."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db_connection.close()

# Lancer le serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
