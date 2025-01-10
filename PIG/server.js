const express = require('express');
const { DynamoDBClient, PutItemCommand, ScanCommand } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, marshall, unmarshall } = require('@aws-sdk/lib-dynamodb');
const bodyParser = require('body-parser');

// Configuration de AWS DynamoDB avec SDK v3
const client = new DynamoDBClient({ region: 'us-east-1' });  // Remplace par ta région
const dynamoDB = DynamoDBDocumentClient.from(client);

const app = express();
app.use(bodyParser.json());

// Route pour récupérer les événements d'une association
app.get('/api/assos', async (req, res) => {
  try {
    const params = {
      TableName: 'assos',
    };

    const data = await dynamoDB.send(new ScanCommand(params));
    const items = data.Items.map((item) => unmarshall(item));
    res.json(items);
  } catch (error) {
    console.error(error);
    res.status(500).send('Erreur serveur');
  }
});

// Route pour ajouter un événement
app.post('/api/assos', async (req, res) => {
  const { nomAsso, description, date } = req.body;

  const params = {
    TableName: 'assos',
    Item: marshall({
      idEvent: `${Date.now()}`, // ID unique basé sur le timestamp
      nomAsso,
      description,
      date,
    }),
  };

  try {
    await dynamoDB.send(new PutItemCommand(params));
    res.status(201).send('Événement ajouté');
  } catch (error) {
    console.error(error);
    res.status(500).send('Erreur serveur');
  }
});

// Lancer le serveur sur le port 3000
app.listen(3000, () => {
  console.log('Serveur Node.js en écoute sur http://localhost:3000');
});
