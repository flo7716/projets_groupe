const express = require('express');
const { DynamoDBClient, PutItemCommand, ScanCommand } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, marshall, unmarshall } = require('@aws-sdk/lib-dynamodb');
const bodyParser = require('body-parser');

// Configuration de AWS DynamoDB avec SDK v3 (région mise à jour pour Paris)
const client = new DynamoDBClient({ region: 'eu-west-3' });  // Région Paris
const dynamoDB = DynamoDBDocumentClient.from(client);

const app = express();
app.use(bodyParser.json());

// Middleware pour gérer les headers CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Route de test pour vérifier si le serveur fonctionne
app.get('/', (req, res) => {
  res.send('Serveur Express fonctionne correctement');
});

// Route pour récupérer les événements d'une association depuis DynamoDB
app.get('/api/assos', async (req, res) => {
  try {
    const params = {
      TableName: 'assos',  // Table DynamoDB
    };

    const data = await dynamoDB.send(new ScanCommand(params));
    const items = data.Items.map((item) => unmarshall(item));
    res.json(items);
  } catch (error) {
    console.error(error);
    res.status(500).send('Erreur serveur lors de la récupération des événements');
  }
});

// Route pour ajouter un événement à la table DynamoDB
app.post('/api/assos', async (req, res) => {
  const { nomAsso, description, date } = req.body;

  const params = {
    TableName: 'assos',  // Table DynamoDB
    Item: marshall({
      idEvent: `${Date.now()}`,  // ID unique basé sur le timestamp
      nomAsso,
      description,
      date,
    }),
  };

  try {
    await dynamoDB.send(new PutItemCommand(params));
    res.status(201).send('Événement ajouté avec succès');
  } catch (error) {
    console.error(error);
    res.status(500).send('Erreur serveur lors de l\'ajout de l\'événement');
  }
});

// Lancer le serveur sur le port 3000
app.listen(3000, () => {
  console.log('Serveur Node.js en écoute sur http://localhost:3000');
});
