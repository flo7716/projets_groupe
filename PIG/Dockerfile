# Image de base pour Node.js
FROM node:18

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de package et installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le reste des fichiers
COPY . .

# Exposer le port pour l'application
EXPOSE 3001

# Commande de démarrage
CMD ["node", "server.js"]
