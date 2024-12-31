from transformers import pipeline
import pymysql

def filter_articles():
    summarizer = pipeline("summarization")

    connection = pymysql.connect(host='localhost', user='root', password='password', database='news_db')
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id, summary FROM articles WHERE summary IS NOT NULL")
    articles = cursor.fetchall()

    for article in articles:
        summarized_text = summarizer(article['summary'], max_length=50, min_length=25, do_sample=False)[0]['summary_text']
        cursor.execute("""
            UPDATE articles SET summary = %s WHERE id = %s
        """, (summarized_text, article['id']))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    filter_articles()
