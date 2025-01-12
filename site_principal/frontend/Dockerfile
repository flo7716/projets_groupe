# Utiliser une image de base avec Node.js
FROM node:16

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY ./frontend /app

# Installer les dépendances
RUN npm install

# Exposer le port sur lequel React va tourner
EXPOSE 3000

# Lancer l'application React
CMD ["npm", "start"]
