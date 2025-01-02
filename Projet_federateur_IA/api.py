from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def connect_db():
    connection = pymysql.connect(host='localhost', user='XXXX', password='XXXXXXXX', database='XXXXXXX')
    cursor= connection.cursor(pymysql.cursors.DictCursor)
    return connection,cursor

def get_articles():
    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    cursor.close()
    connection.close()
    return articles

def get_article_by_name(article_name):
    connection, cursor = connect_db()

    cursor.execute("SELECT * FROM articles WHERE title = %s", (article_name, ))
    article = cursor.fetchone()

    cursor.close()
    connection.close()
    return article

def get_article_by_category(category_name):
    connection, cursor = connect_db()

    cursor.execute("SELECT * FROM articles WHERE category = %s", (category_name,))
    article = cursor.fetchone()

    cursor.close()
    connection.close()
    return article

def delete_article(article_id):
    connection = pymysql.connect(host='localhost', user='XXXX', password='XXXXXXXX', database='XXXXXXX')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return True


@app.route("/api/articles", methods=["GET"])
def api_articles():
    return jsonify(get_articles())

if __name__ == "__main__":
    app.run(debug=True)