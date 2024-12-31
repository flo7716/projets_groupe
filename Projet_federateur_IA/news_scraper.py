import requests
from bs4 import BeautifulSoup
import pymysql

def scrape_news():
    url = "https://techcrunch.com"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        news_data = []

        for article in articles:
            title = article.find('h2').get_text(strip=True) if article.find('h2') else None
            link = article.find('a')['href'] if article.find('a') else None
            summary = article.find('p').get_text(strip=True) if article.find('p') else None

            if title and link:
                news_data.append({"title": title, "link": link, "summary": summary})

        save_to_database(news_data)
    else:
        print(f"Failed to scrape news. Status code: {response.status_code}")

def save_to_database(news_data):
    connection = pymysql.connect(host='localhost', user='root', password='password', database='news_db')
    cursor = connection.cursor()

    for news in news_data:
        cursor.execute("""
            INSERT INTO articles (title, link, summary) VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE summary=VALUES(summary)
        """, (news['title'], news['link'], news['summary']))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    scrape_news()