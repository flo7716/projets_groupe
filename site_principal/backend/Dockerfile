# Utiliser une image de base avec Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY ./backend /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application Flask va tourner
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]
