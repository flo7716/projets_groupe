import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fonction pour récupérer les articles depuis l'API Flask
    const fetchArticles = async () => {
      try {
        const response = await axios.get('http://13.36.211.1:5000/api/articles');
        setArticles(response.data);
        setLoading(false);
      } catch (err) {
        setError('Erreur lors du chargement des articles');
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="App">
      <h1>Latest News Articles</h1>
      <div className="articles-container">
        {articles.map((article, index) => (
          <div key={index} className="article">
            <h2>{article.title}</h2>
            <p><strong>Published on: </strong>{article.datePublication}</p>
            <p>{article.summary}</p>
            {article.image_url && <img src={article.image_url} alt={article.title} />}
            <p><a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a></p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
