const express = require('express');
const AWS = require('aws-sdk');
const bodyParser = require('body-parser');

// Configuration de AWS DynamoDB
AWS.config.update({
  region: 'us-east-1', // Remplace par ta région AWS
});

const dynamoDB = new AWS.DynamoDB.DocumentClient();

const app = express();
app.use(bodyParser.json());

// Route pour récupérer les événements d'une association
app.get('/api/assos', async (req, res) => {
  try {
    const params = {
      TableName: 'assos', // Remplace par ton nom de table DynamoDB
    };

    const data = await dynamoDB.scan(params).promise();
    res.json(data.Items);
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
    Item: {
      idEvent: `${Date.now()}`,  // Utilisation de l'ID basé sur l'heure (id unique)
      nomAsso,
      description,
      date,
    },
  };

  try {
    await dynamoDB.put(params).promise();
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
