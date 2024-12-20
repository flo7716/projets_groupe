import instaloader
import mysql.connector
from mysql.connector import connect, Error

def connect_to_db():
    """Connexion à la base de données MySQL."""
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="instagram_scraper",
            password="instagram_scraper",
            database="pig"
        )
        if connection.is_connected():
            print("Connecté à la base de données.")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None


def insert_event(connection, table, data):
    """Insertion d'événement dans la table spécifiée."""
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


def update_instagram_link(asso_name, instagram_link, db_connection):
    """Mettre à jour le lien Instagram dans la table ASSOCIATION."""
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT idAsso FROM ASSOCIATION WHERE nomAsso = %s", (asso_name,))
        result = cursor.fetchone()

        if result:
            asso_id = result[0]
            cursor.execute("UPDATE ASSOCIATION SET compteInstagram = %s WHERE idAsso = %s", (instagram_link, asso_id))
            db_connection.commit()
            print(f"Compte Instagram pour {asso_name} mis à jour avec succès.")
        else:
            print(f"Association {asso_name} non trouvée.")
        cursor.close()
    except Error as e:
        print(f"Erreur lors de la mise à jour de l'Instagram pour {asso_name} : {e}")


def scrape_posts(account_name, connection, instagram_link, instagram_user, instagram_pass):
    """Récupère les posts d'un compte et les insère en base."""
    # Initialiser instaloader
    loader = instaloader.Instaloader()

    try:
        # Authentification avec les identifiants fournis par l'utilisateur
        if not loader.context.is_logged_in:
            loader.context.login(instagram_user, instagram_pass)  # Utilise l'input de l'utilisateur

        # Charger les posts du compte
        profile = instaloader.Profile.from_username(loader.context, account_name)
        print(f"Scraping des posts pour le compte : {profile.username}")

        # Mettre à jour le lien Instagram dans la base de données
        update_instagram_link(account_name, instagram_link, connection)

        for post in profile.get_posts():
            # Extraire les informations nécessaires
            event_id = post.shortcode
            event_date = post.date.date()
            description = post.caption or "Pas de description."
            location = post.location.name if post.location else "Lieu non spécifié"

            # Déterminer la table (asso ou entreprise)
            if "asso" in description.lower():
                table = "EVENEMENT_ORGANISE_PAR_ASSO"
                organizer_id = "ID_ASSO_EXAMPLE"
            else:
                table = "EVENEMENT_ORGANISE_PAR_ENTREPRISE"
                organizer_id = "ID_ENTREPRISE_EXAMPLE"

            # Insérer en base
            event_data = (organizer_id, event_id, event_date, location, description)
            insert_event(connection, table, event_data)

    except Exception as e:
        print(f"Erreur lors du scraping des posts : {e}")


if __name__ == "__main__":
    # Demander à l'utilisateur son identifiant et mot de passe Instagram
    instagram_user = input("Entrez votre identifiant Instagram : ")
    instagram_pass = input("Entrez votre mot de passe Instagram : ")

    # Connexion à la base de données
    db_connection = connect_to_db()
    if not db_connection:
        exit()

    # Comptes à scraper (dictionnaire avec noms d'assos et leurs liens Instagram)
    instagram_accounts = {
        "Scrypt": "https://www.instagram.com/ipsa.scrypt/"
    }

    # Scraper chaque compte
    for account_name, instagram_link in instagram_accounts.items():
        scrape_posts(account_name, db_connection, instagram_link, instagram_user, instagram_pass)

    # Fermer la connexion à la base de données
    db_connection.close()
    print("Fin du script.")
