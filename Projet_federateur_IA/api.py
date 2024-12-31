from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def get_articles():
    connection = pymysql.connect(host='localhost', user='root', password='password', database='news_db')
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    cursor.close()
    connection.close()
    return articles

@app.route("/api/articles", methods=["GET"])
def api_articles():
    return jsonify(get_articles())

if __name__ == "__main__":
    app.run(debug=True)