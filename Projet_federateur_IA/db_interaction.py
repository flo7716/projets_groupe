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

def save_articles_to_db(articles):
    for article in articles:
        save_to_database(article['url'], article['title'], article['summary'], article['content'])

if __name__ == "__main__":
    articles_to_save = [
        {"url": "https://techcrunch.com/sample-article", "title": "Sample Title", "summary": "Sample Summary", "content": "Article Content"}
    ]
    save_articles_to_db(articles_to_save)
