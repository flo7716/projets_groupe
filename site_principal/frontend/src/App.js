import React, { useState, useEffect } from 'react';

function App() {
  const [articles, setArticles] = useState([]);
  const [associations, setAssociations] = useState([]);
  const [articleTitle, setArticleTitle] = useState('');
  const [articleContent, setArticleContent] = useState('');
  const [associationName, setAssociationName] = useState('');
  const [associationDescription, setAssociationDescription] = useState('');
  const [message, setMessage] = useState('');

  // Récupérer les articles
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/articles');
        const data = await response.json();
        if (response.ok) {
          setArticles(data.articles);
        } else {
          setMessage(data.message);
        }
      } catch (error) {
        setMessage('Erreur de connexion au serveur pour les articles.');
      }
    };

    fetchArticles();
  }, []);

  // Récupérer les associations
  useEffect(() => {
    const fetchAssociations = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/associations');
        const data = await response.json();
        if (response.ok) {
          setAssociations(data.associations);
        } else {
          setMessage(data.message);
        }
      } catch (error) {
        setMessage('Erreur de connexion au serveur pour les associations.');
      }
    };

    fetchAssociations();
  }, []);

  // Ajouter un article
  const handleArticleSubmit = async (e) => {
    e.preventDefault();
    
    const newArticle = { title: articleTitle, content: articleContent };

    try {
      const response = await fetch('http://localhost:5000/api/articles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newArticle),
      });

      const data = await response.json();

      if (response.ok) {
        setArticles([...articles, data.article]);
        setArticleTitle('');
        setArticleContent('');
        setMessage('Article ajouté avec succès!');
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage('Erreur lors de l\'ajout de l\'article.');
    }
  };

  // Ajouter une association
  const handleAssociationSubmit = async (e) => {
    e.preventDefault();
    
    const newAssociation = { name: associationName, description: associationDescription };

    try {
      const response = await fetch('http://localhost:5000/api/associations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newAssociation),
      });

      const data = await response.json();

      if (response.ok) {
        setAssociations([...associations, data.association]);
        setAssociationName('');
        setAssociationDescription('');
        setMessage('Association ajoutée avec succès!');
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage('Erreur lors de l\'ajout de l\'association.');
    }
  };

  return (
    <div>
      <h1>Liste des Articles</h1>
      {message && <p>{message}</p>}
      
      <form onSubmit={handleArticleSubmit}>
        <div>
          <label>Titre</label>
          <input
            type="text"
            value={articleTitle}
            onChange={(e) => setArticleTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Contenu</label>
          <textarea
            value={articleContent}
            onChange={(e) => setArticleContent(e.target.value)}
            required
          />
        </div>
        <button type="submit">Ajouter Article</button>
      </form>

      <ul>
        {articles.map((article) => (
          <li key={article.id}>
            <h3>{article.title}</h3>
            <p>{article.content}</p>
          </li>
        ))}
      </ul>

      <h1>Liste des Associations</h1>
      
      <form onSubmit={handleAssociationSubmit}>
        <div>
          <label>Nom de l'Association</label>
          <input
            type="text"
            value={associationName}
            onChange={(e) => setAssociationName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            value={associationDescription}
            onChange={(e) => setAssociationDescription(e.target.value)}
            required
          />
        </div>
        <button type="submit">Ajouter Association</button>
      </form>

      <ul>
        {associations.map((association) => (
          <li key={association.id}>
            <h3>{association.name}</h3>
            <p>{association.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
