import React, { useEffect, useState } from 'react';

function ArticleList() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch('/api/articles')
      .then(response => response.json())
      .then(data => setArticles(data))
      .catch(error => console.error('Error fetching articles:', error));
  }, []);

  return (
    <div>
      <h1>Liste des articles</h1>
      {articles.length === 0 ? (
        <p>Pas d'articles disponibles</p>
      ) : (
        <ul>
          {articles.map((article, index) => (
            <li key={index}>
              <h2>{article.title}</h2>
              <p>{article.summary}</p>
              <a href={article.url}>Lire plus</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ArticleList;
