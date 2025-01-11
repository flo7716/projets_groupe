const express = require('express');
const { DynamoDBClient, PutItemCommand, ScanCommand } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, marshall, unmarshall } = require('@aws-sdk/lib-dynamodb');
const bodyParser = require('body-parser');

const client = new DynamoDBClient({ region: 'eu-west-3' });
const dynamoDB = DynamoDBDocumentClient.from(client);

const app = express();
app.use(bodyParser.json());

// Middleware CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Route pour récupérer les articles
app.get('/api/articles', async (req, res) => {
  try {
    const params = { TableName: 'articles' };
    const data = await dynamoDB.send(new ScanCommand(params));
    if (!data.Items) {
      return res.status(404).send('Aucun article trouvé');
    }

    const items = data.Items.map((item) => unmarshall(item));
    res.json(items);
  } catch (error) {
    console.error('Erreur lors de la récupération des articles:', error);
    res.status(500).send('Erreur serveur lors de la récupération des articles');
  }
});

// Route pour ajouter un article
app.post('/api/articles', async (req, res) => {
  const { titre, contenu, auteur } = req.body;

  if (!titre || !contenu || !auteur) {
    return res.status(400).send('Les informations de l\'article sont manquantes');
  }

  const params = {
    TableName: 'articles',
    Item: marshall({
      idArticle: `${Date.now()}`,  // ID unique basé sur le timestamp
      titre,
      contenu,
      auteur,
    }),
  };

  try {
    await dynamoDB.send(new PutItemCommand(params));
    res.status(201).send('Article ajouté avec succès');
  } catch (error) {
    console.error('Erreur lors de l\'ajout de l\'article:', error);
    res.status(500).send('Erreur serveur lors de l\'ajout de l\'article');
  }
});

// Lancer le serveur pour les articles
app.listen(4000, '0.0.0.0', () => {
  console.log('Serveur Articles en écoute sur http://articles.local:4000');
});
