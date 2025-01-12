# Utilisation d'une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Installer Boto3 pour DynamoDB
RUN pip install boto3

# Exposer le port sur lequel Flask sera exécuté
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]
