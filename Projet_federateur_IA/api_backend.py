import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def save_to_database(url, title, summary, article_text):
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
        )
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO articles (link, title, summary, content) 
            VALUES (%s, %s, %s, %s)
        """, (url, title, summary, article_text))
        connection.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    save_to_database('https://techcrunch.com/2025/01/06/lucid-meets-production-target-with-9029-ev-deliveries-in-2024/', 'Sample Title', 'This is a summary', 'Article content goes here...')
