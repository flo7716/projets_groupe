const express = require('express');
const AWS = require('aws-sdk');
const bodyParser = require('body-parser');
const { fetchArticles } = require('./scraper');  // Import du scraper

const app = express();
const port = 5001;

// Configurer AWS DynamoDB
AWS.config.update({
  region: 'us-east-1',  // Région où tu as configuré DynamoDB
});

const docClient = new AWS.DynamoDB.DocumentClient();

app.use(bodyParser.json());  // Permet d'analyser les requêtes JSON

// Endpoint pour récupérer les articles
app.get('/api/articles', async (req, res) => {
  try {
    const articles = await fetchArticles();
    res.json({ message: "Articles récupérés avec succès!", articles });
  } catch (err) {
    res.status(500).json({ message: 'Erreur lors de la récupération des articles.', error: err });
  }
});

// Endpoint pour ajouter un article
app.post('/api/articles', async (req, res) => {
  const { title, content } = req.body;

  if (!title || !content) {
    return res.status(400).json({ message: 'Le titre et le contenu de l\'article sont requis.' });
  }

  const params = {
    TableName: 'Articles',  // Table DynamoDB pour stocker les articles
    Item: {
      id: AWS.util.uuid.v4(),  // Génère un ID unique pour chaque article
      title: title,
      content: content,
      createdAt: new Date().toISOString(),
    },
  };

  try {
    // Insérer l'article dans DynamoDB
    await docClient.put(params).promise();
    res.status(201).json({ message: 'Article ajouté avec succès!', article: params.Item });
  } catch (error) {
    console.error('Erreur lors de l\'ajout de l\'article:', error);
    res.status(500).json({ message: 'Erreur lors de l\'ajout de l\'article.', error });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
