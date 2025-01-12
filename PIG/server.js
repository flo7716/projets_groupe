const express = require('express');
const { DynamoDBClient, PutItemCommand, ScanCommand } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, marshall } = require('@aws-sdk/lib-dynamodb');
const { unmarshall } = require('@aws-sdk/util-dynamodb');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

// Configuration AWS DynamoDB
const client = new DynamoDBClient({ region: 'eu-west-3' });
const dynamoDB = DynamoDBDocumentClient.from(client);

const app = express();
app.use(bodyParser.json());

// Logger
const logFilePath = path.join(__dirname, 'logs', 'pig.log');
function logEvent(message) {
  fs.appendFileSync(logFilePath, `${new Date().toISOString()} - ${message}\n`);
}

// Middleware pour gérer les headers CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Route de test
app.get('/', (req, res) => {
  res.send('Serveur PIG fonctionne correctement');
  logEvent('Route principale "/" appelée avec succès');
});

// Récupérer les associations
app.get('/api/assos', async (req, res) => {
  try {
    const params = { TableName: 'assos' };
    const data = await dynamoDB.send(new ScanCommand(params));

    if (!data.Items) {
      res.status(404).send('Aucune association trouvée');
      logEvent('Aucune association trouvée lors de la récupération');
      return;
    }

    const items = data.Items.map((item) => unmarshall(item));
    res.json(items);
    logEvent(`Associations récupérées avec succès : ${items.length} éléments`);
  } catch (error) {
    console.error('Erreur lors de la récupération des associations:', error);
    res.status(500).send('Erreur serveur lors de la récupération des associations');
    logEvent('Erreur serveur lors de la récupération des associations');
  }
});

// Ajouter une association
app.post('/api/assos', async (req, res) => {
  const { nomAsso, description, date } = req.body;

  if (!nomAsso || !description || !date) {
    res.status(400).send('Informations manquantes');
    logEvent('Tentative d\'ajout avec informations manquantes');
    return;
  }

  const params = {
    TableName: 'assos',
    Item: marshall({
      idEvent: `${Date.now()}`,
      nomAsso,
      description,
      date,
    }),
  };

  try {
    await dynamoDB.send(new PutItemCommand(params));
    res.status(201).send('Association ajoutée avec succès');
    logEvent(`Association ajoutée : ${nomAsso}`);
  } catch (error) {
    console.error('Erreur lors de l\'ajout de l\'association:', error);
    res.status(500).send('Erreur serveur lors de l\'ajout de l\'association');
    logEvent('Erreur serveur lors de l\'ajout de l\'association');
  }
});

// Lancer le serveur
const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Serveur PIG en écoute sur http://localhost:${PORT}`);
  logEvent(`Serveur démarré sur le port ${PORT}`);
});
