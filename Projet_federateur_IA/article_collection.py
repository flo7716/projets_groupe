import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_article_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        full_url = urljoin(url, link)
        article_links.add(full_url)
        if len(article_links) >= 10:
            break

    return list(article_links)

if __name__ == "__main__":
    base_url = 'https://techcrunch.com/'
    article_urls = extract_article_links(base_url)
    for article in article_urls:
        print(article)
