const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'ta_clé_secrète';

function authenticate(req, res, next) {
    const token = req.headers['authorization'] && req.headers['authorization'].split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Token manquant' });
    }

    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err) {
            return res.status(401).json({ error: 'Token invalide' });
        }

        req.user = decoded; // Ajoute les informations de l'utilisateur à la requête
        next(); // Passe à la route suivante
    });
}

module.exports = authenticate;
