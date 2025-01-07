const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const connection = require('./db');
const router = express.Router();

// Route pour l'inscription d'un utilisateur
router.post('/signup', async (req, res) => {
    const { username, password, role, nomAsso } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10); // Hash du mot de passe

    const sql = 'INSERT INTO users (username, password, role, nomAsso) VALUES (?, ?, ?, ?)';
    connection.query(sql, [username, hashedPassword, role, nomAsso], (err, results) => {
        if (err) {
            console.error('Erreur lors de l\'inscription', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(201).send('Utilisateur créé');
        }
    });
});

// Route pour la connexion d'un utilisateur
router.post('/login', (req, res) => {
    const { username, password } = req.body;

    const sql = 'SELECT * FROM users WHERE username = ?';
    connection.query(sql, [username], async (err, results) => {
        if (err) {
            console.error('Erreur lors de la connexion', err);
            return res.status(500).send('Erreur serveur');
        }

        const user = results[0];
        if (!user) {
            return res.status(400).json({ error: 'Utilisateur non trouvé' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ error: 'Mot de passe incorrect' });
        }

        // Générer un token JWT
        const token = jwt.sign(
            { id: user.id, username: user.username, role: user.role, nomAsso: user.nomAsso },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.json({ token });
    });
});

module.exports = router;
