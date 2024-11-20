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


# Fonctions CRUD pour la table ASSOCIATION
def create_association(connection, id_asso, nom_asso, domaine_asso):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ASSOCIATION (idAsso, nomAsso, domaineAsso) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_asso, nom_asso, domaine_asso))
        connection.commit()
        print(f"Association {nom_asso} ajoutée.")
    except Error as e:
        print(f"Erreur lors de l'insertion de l'association : {e}")


def read_associations(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM ASSOCIATION"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Liste des associations :")
        for row in results:
            print(row)
    except Error as e:
        print(f"Erreur lors de la lecture des associations : {e}")


def update_association(connection, id_asso, nom_asso=None, domaine_asso=None):
    try:
        cursor = connection.cursor()
        updates = []
        if nom_asso:
            updates.append(f"nomAsso='{nom_asso}'")
        if domaine_asso:
            updates.append(f"domaineAsso='{domaine_asso}'")
        if updates:
            query = f"UPDATE ASSOCIATION SET {', '.join(updates)} WHERE idAsso=%s"
            cursor.execute(query, (id_asso,))
            connection.commit()
            print(f"Association {id_asso} mise à jour.")
    except Error as e:
        print(f"Erreur lors de la mise à jour de l'association : {e}")


def delete_association(connection, id_asso):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM ASSOCIATION WHERE idAsso=%s"
        cursor.execute(query, (id_asso,))
        connection.commit()
        print(f"Association {id_asso} supprimée.")
    except Error as e:
        print(f"Erreur lors de la suppression de l'association : {e}")


# Fonctions CRUD pour la table ENTREPRISE
def create_entreprise(connection, id_entreprise, nom_entreprise, domaine_entreprise):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ENTREPRISE (idEntreprise, nomEntreprise, domaineEntreprise) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_entreprise, nom_entreprise, domaine_entreprise))
        connection.commit()
        print(f"Entreprise {nom_entreprise} ajoutée.")
    except Error as e:
        print(f"Erreur lors de l'insertion de l'entreprise : {e}")


def read_entreprises(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM ENTREPRISE"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Liste des entreprises :")
        for row in results:
            print(row)
    except Error as e:
        print(f"Erreur lors de la lecture des entreprises : {e}")


def update_entreprise(connection, id_entreprise, nom_entreprise=None, domaine_entreprise=None):
    try:
        cursor = connection.cursor()
        updates = []
        if nom_entreprise:
            updates.append(f"nomEntreprise='{nom_entreprise}'")
        if domaine_entreprise:
            updates.append(f"domaineEntreprise='{domaine_entreprise}'")
        if updates:
            query = f"UPDATE ENTREPRISE SET {', '.join(updates)} WHERE idEntreprise=%s"
            cursor.execute(query, (id_entreprise,))
            connection.commit()
            print(f"Entreprise {id_entreprise} mise à jour.")
    except Error as e:
        print(f"Erreur lors de la mise à jour de l'entreprise : {e}")


def delete_entreprise(connection, id_entreprise):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM ENTREPRISE WHERE idEntreprise=%s"
        cursor.execute(query, (id_entreprise,))
        connection.commit()
        print(f"Entreprise {id_entreprise} supprimée.")
    except Error as e:
        print(f"Erreur lors de la suppression de l'entreprise : {e}")


# Fonctions CRUD pour les événements (table dynamique)
def create_event(connection, table, organizer_id, event_id, date_event, lieu_event, description_event):
    try:
        cursor = connection.cursor()
        query = f"""
        INSERT INTO {table} (id{table[:-1]}, idEvent, dateEvent, lieuEvent, descriptionEvent)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (organizer_id, event_id, date_event, lieu_event, description_event))
        connection.commit()
        print(f"Événement {event_id} ajouté dans {table}.")
    except Error as e:
        print(f"Erreur lors de l'ajout de l'événement dans {table} : {e}")


def read_events(connection, table):
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Liste des événements dans {table} :")
        for row in results:
            print(row)
    except Error as e:
        print(f"Erreur lors de la lecture des événements dans {table} : {e}")


def update_event(connection, table, organizer_id, event_id, date_event=None, lieu_event=None, description_event=None):
    try:
        cursor = connection.cursor()
        updates = []
        if date_event:
            updates.append(f"dateEvent='{date_event}'")
        if lieu_event:
            updates.append(f"lieuEvent='{lieu_event}'")
        if description_event:
            updates.append(f"descriptionEvent='{description_event}'")
        if updates:
            query = f"""
            UPDATE {table} SET {', '.join(updates)} 
            WHERE id{table[:-1]}=%s AND idEvent=%s
            """
            cursor.execute(query, (organizer_id, event_id))
            connection.commit()
            print(f"Événement {event_id} dans {table} mis à jour.")
    except Error as e:
        print(f"Erreur lors de la mise à jour de l'événement dans {table} : {e}")


def delete_event(connection, table, organizer_id, event_id):
    try:
        cursor = connection.cursor()
        query = f"DELETE FROM {table} WHERE id{table[:-1]}=%s AND idEvent=%s"
        cursor.execute(query, (organizer_id, event_id))
        connection.commit()
        print(f"Événement {event_id} supprimé de {table}.")
    except Error as e:
        print(f"Erreur lors de la suppression de l'événement dans {table} : {e}")


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
