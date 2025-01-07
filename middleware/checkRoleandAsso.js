const express = require('express');
const bodyParser = require('body-parser');
const connection = require('./db');
const authenticate = require('./middleware/authenticate');
const checkRoleAndAsso = require('./middleware/checkRoleAndAsso');

const app = express();
const port = 3000;

// Middleware pour analyser le corps des requêtes
app.use(bodyParser.json());

// Route protégée pour ajouter un événement, accessible à tous les admins ou aux membres d'une association spécifique
app.post('/events', authenticate, checkRoleAndAsso('admin', 'any'), (req, res) => {
    const { nomAsso, description, date } = req.body;
    const sql = 'INSERT INTO events (nomAsso, description, date) VALUES (?, ?, ?)';
    connection.query(sql, [nomAsso, description, date], (err, results) => {
        if (err) {
            console.error('Erreur lors de l\'ajout de l\'événement', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(201).send('Événement ajouté');
        }
    });
});

// Route pour récupérer tous les événements (accessible sans authentification)
app.get('/events', (req, res) => {
    connection.query('SELECT * FROM events', (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération des événements', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(200).json(results);
        }
    });
});

// Route pour mettre à jour un événement, uniquement accessible aux admins ou membres d'une association spécifique
app.put('/events/:id', authenticate, checkRoleAndAsso('admin', 'any'), (req, res) => {
    const { id } = req.params;
    const { nomAsso, description, date } = req.body;
    const sql = 'UPDATE events SET nomAsso = ?, description = ?, date = ? WHERE idEvent = ?';
    connection.query(sql, [nomAsso, description, date, id], (err, results) => {
        if (err) {
            console.error('Erreur lors de la mise à jour de l\'événement', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(200).send('Événement mis à jour');
        }
    });
});

// Route pour supprimer un événement, uniquement accessible aux admins ou membres d'une association spécifique
app.delete('/events/:id', authenticate, checkRoleAndAsso('admin', 'any'), (req, res) => {
    const { id } = req.params;
    const sql = 'DELETE FROM events WHERE idEvent = ?';
    connection.query(sql, [id], (err, results) => {
        if (err) {
            console.error('Erreur lors de la suppression de l\'événement', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(200).send('Événement supprimé');
        }
    });
});

// Démarrage du serveur
app.listen(port, () => {
    console.log(`Serveur démarré sur http://localhost:${port}`);
});
