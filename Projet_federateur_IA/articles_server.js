const express = require('express');
const bodyParser = require('body-parser');
const { DynamoDB } = require('aws-sdk');

const app = express();
const port = 3000;

// Configuration de DynamoDB
const dynamoDb = new DynamoDB.DocumentClient();
const tableName = 'articles';

// Middleware pour parser le JSON
app.use(bodyParser.json());

// Route pour récupérer tous les articles
app.get('/articles', async (req, res) => {
    try {
        const params = {
            TableName: tableName
        };

        const result = await dynamoDb.scan(params).promise();
        res.json(result.Items);
    } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
        res.status(500).send('Erreur serveur');
    }
});

// Route pour ajouter un article
app.post('/articles', async (req, res) => {
    const article = req.body;
    
    const params = {
        TableName: tableName,
        Item: article
    };

    try {
        await dynamoDb.put(params).promise();
        res.status(201).send('Article ajouté');
    } catch (error) {
        console.error('Erreur lors de l\'ajout de l\'article:', error);
        res.status(500).send('Erreur serveur');
    }
});

// Lancer le serveur
app.listen(port, () => {
    console.log(`Serveur backend démarré sur http://localhost:${port}`);
});
