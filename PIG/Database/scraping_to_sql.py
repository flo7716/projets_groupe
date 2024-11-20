import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import datetime

# Fonction pour se connecter à la base de données MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="your_host",
            user="your_user",
            password="your_password",
            database="school_events"
        )
        if connection.is_connected():
            print("Connecté à la base de données")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

# Fonction pour insérer un événement dans la base de données
def insert_event(connection, table_name, event_data):
    try:
        cursor = connection.cursor()
        if table_name == "EVENEMENT_ORGANISE_PAR_ASSO":
            sql_query = """
                INSERT INTO EVENEMENT_ORGANISE_PAR_ASSO (idAsso, idEvent, dateEvent, lieuEvent, descriptionEvent)
                VALUES (%s, %s, %s, %s, %s)
            """
        elif table_name == "EVENEMENT_ORGANISE_PAR_ENTREPRISE":
            sql_query = """
                INSERT INTO EVENEMENT_ORGANISE_PAR_ENTREPRISE (idEntreprise, idEvent, dateEvent, lieuEvent, descriptionEvent)
                VALUES (%s, %s, %s, %s, %s)
            """
        else:
            print("Table inconnue")
            return

        cursor.execute(sql_query, event_data)
        connection.commit()
        print(f"Événement ajouté à la table {table_name}")
    except Error as e:
        print(f"Erreur lors de l'insertion : {e}")

# Fonction de scraping
def scrape_events():
    url = "https://www.example.com/events"  # Remplacez par l'URL réelle
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur lors de la récupération de la page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Exemple de structure d'extraction. Adaptez au HTML de la page cible.
    events = []
    event_cards = soup.find_all("div", class_="event-card")  # Adaptez le sélecteur
    for card in event_cards:
        event_id = card["data-id"]  # Identifiant unique de l'événement
        name = card.find("h3", class_="event-name").text.strip()
        date_str = card.find("span", class_="event-date").text.strip()
        location = card.find("span", class_="event-location").text.strip()
        description = card.find("p", class_="event-description").text.strip()

        # Conversion de la date
        event_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

        # Ajout au tableau d'événements
        events.append((event_id, name, event_date, location, description))
    return events

# Script principal
if __name__ == "__main__":
    # Connexion à la base de données
    db_connection = connect_to_db()
    if not db_connection:
        exit()

    # Scraping des événements
    scraped_events = scrape_events()

    # Ajout des événements dans la base de données
    for event in scraped_events:
        # Déterminez ici si l'événement provient d'une association ou d'une entreprise
        if "asso" in event[0]:  # Par exemple, un ID contenant "asso"
            insert_event(
                db_connection, "EVENEMENT_ORGANISE_PAR_ASSO",
                ("ID_ASSO_EXAMPLE", event[0], event[2], event[3], event[4])
            )
        else:
            insert_event(
                db_connection, "EVENEMENT_ORGANISE_PAR_ENTREPRISE",
                ("ID_ENTREPRISE_EXAMPLE", event[0], event[2], event[3], event[4])
            )

    # Fermeture de la connexion
    db_connection.close()
    print("Fin du script")
