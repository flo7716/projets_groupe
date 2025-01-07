-- Créer la base de données "assos"
CREATE DATABASE assos;

-- Utiliser la base de données "assos"
USE assos;

-- Créer la base de données "assos"
CREATE DATABASE assos;

-- Utiliser la base de données "assos"
USE assos;

-- Créer la table "associations" pour stocker les informations sur les associations
CREATE TABLE associations (
    idAsso INT AUTO_INCREMENT PRIMARY KEY,
    nomAsso VARCHAR(255) NOT NULL,
    description TEXT
);

-- Créer la table "events" pour stocker les événements des associations
CREATE TABLE events (
    idEvent INT AUTO_INCREMENT PRIMARY KEY,
    idAsso INT,
    description TEXT,
    dateEvent DATETIME NOT NULL,
    FOREIGN KEY (idAsso) REFERENCES associations(idAsso) ON DELETE CASCADE
);


-- Créer la base de données "news"
CREATE DATABASE news;

-- Utiliser la base de données "news"
USE news;

-- Créer la table "articles" pour stocker les articles d'actualités
CREATE TABLE articles (
    idArticle INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    source VARCHAR(255),
    published_date DATETIME,
    image_url VARCHAR(255)
);

-- Optionnel : Créer une table pour les utilisateurs si nécessaire
-- Créer la table "users" pour stocker les informations des utilisateurs (si tu en as besoin pour le login)
CREATE TABLE users (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('responsable', 'scraper', 'admin') NOT NULL
);
