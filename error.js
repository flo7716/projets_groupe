function errorHandler(err, req, res, next) {
    console.error(err.stack);
    res.status(500).send('Erreur serveur');
}

module.exports = errorHandler;
