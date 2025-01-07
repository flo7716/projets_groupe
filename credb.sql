-- 1. Création de la base de données `users`
CREATE DATABASE users;

-- 2. Création de la table `users` dans la base `users`
USE users;

CREATE TABLE users (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- 3. Création de la base de données `assos` (pour les associations et événements)
CREATE DATABASE assos;

-- 4. Création de la table `assos` dans la base `assos`
USE assos;

CREATE TABLE assos (
    idAsso INT AUTO_INCREMENT PRIMARY KEY,
    nomAsso VARCHAR(255) NOT NULL,
    description TEXT,
    idUser INT,  -- ID de l'utilisateur responsable de l'association
    FOREIGN KEY (idUser) REFERENCES users(idUser)  -- Relation avec la table `users`
);

-- 5. Création de la base de données `news` (pour les articles)
CREATE DATABASE news;

-- 6. Création de la table `articles` dans la base `news`
USE news;

CREATE TABLE articles (
    idArticle INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source VARCHAR(255),
    publish_date DATETIME,
    image_url VARCHAR(255),
    idUser INT,  -- ID de l'utilisateur (scraper) ayant ajouté ou modifié l'article
    FOREIGN KEY (idUser) REFERENCES users(idUser)  -- Relation avec la table `users`
);
