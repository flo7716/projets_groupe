import httpx
import json
from typing import Dict
from urllib.parse import quote
import mysql.connector
from mysql.connector import connect, Error
import datetime
from dotenv import load_dotenv

INSTAGRAM_DOCUMENT_ID = "8845758582119845"  # Instagram post document ID


def connect_to_db():
    """Connect to the MySQL database using instagram scraper account"""
    try:
        # Connexion à MySQL 
        connection = mysql.connector.connect(
            user='instagram_scraper'@'localhost',
            password='instagram_scraper',
            database='pig'
        )
        
        # Vérifier la connexion
        if connection.is_connected():
            print("Connecté à la base de données via auth_socket")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None


def insert_event(connection, table, data):
    """Insert event into the appropriate table."""
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
        print(f"Erreur lors de l'insertion de l'événement dans {table} : {e}")


def scrape_post_and_store(url_or_shortcode: str, connection):
    """
    Scrape Instagram post data and store relevant information in the database.
    """
    # Scrape the Instagram post
    if "http" in url_or_shortcode:
        shortcode = url_or_shortcode.split("/p/")[-1].split("/")[0]
    else:
        shortcode = url_or_shortcode
    print(f"Scraping Instagram post: {shortcode}")

    variables = quote(json.dumps({
        'shortcode': shortcode,
        'fetch_tagged_user_count': None,
        'hoisted_comment_id': None,
        'hoisted_reply_id': None
    }, separators=(',', ':')))
    body = f"variables={variables}&doc_id={INSTAGRAM_DOCUMENT_ID}"
    url = "https://www.instagram.com/graphql/query"

    try:
        result = httpx.post(
            url=url,
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=body
        )
        data = json.loads(result.content)
        post_data = data["data"]["xdt_shortcode_media"]

        # Extract relevant data
        event_id = post_data["id"]
        description = post_data.get("edge_media_to_caption", {}).get("edges", [])[0].get("node", {}).get("text", "")
        location = post_data.get("location", {}).get("name", "Lieu non spécifié")
        timestamp = post_data["taken_at_timestamp"]
        event_date = datetime.datetime.fromtimestamp(timestamp).date()

        # Determine the organizer (example logic)
        if "asso" in description.lower():
            table = "EVENEMENT_ORGANISE_PAR_ASSO"
            organizer_id = "ID_ASSO_EXAMPLE"
        else:
            table = "EVENEMENT_ORGANISE_PAR_ENTREPRISE"
            organizer_id = "ID_ENTREPRISE_EXAMPLE"

        # Insert into the database
        event_data = (organizer_id, event_id, event_date, location, description)
        insert_event(connection, table, event_data)

    except Exception as e:
        print(f"Erreur lors du scraping ou de l'insertion en base : {e}")


if __name__ == "__main__":
    # Connect to the database
    db_connection = connect_to_db()
    if not db_connection:
        exit()

    # Example post URLs
    instagram_posts = [
        "https://www.instagram.com/p/CuE2WNQs6vH/",
        "https://www.instagram.com/p/CvX0y3Vx1Ag/"
    ]

    # Scrape and store each post
    for post_url in instagram_posts:
        scrape_post_and_store(post_url, db_connection)

    # Close the database connection
    db_connection.close()
    print("Fin du script")
