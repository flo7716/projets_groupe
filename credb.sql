-- Create the assos database and its tables
CREATE DATABASE IF NOT EXISTS assos;

USE assos;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS USER (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    nomUser VARCHAR(255) NOT NULL,
    prenomUser VARCHAR(255) NOT NULL,
    emailUser VARCHAR(255) NOT NULL UNIQUE,
    passwordUser VARCHAR(255) NOT NULL,
    roleUser ENUM('admin', 'president') NOT NULL
);

-- Table des associations
CREATE TABLE IF NOT EXISTS ASSOCIATION (
    idAsso INT AUTO_INCREMENT PRIMARY KEY,
    nomAsso VARCHAR(255) NOT NULL UNIQUE,
    domaineAsso VARCHAR(255) NOT NULL,
    presidentId INT NOT NULL,
    FOREIGN KEY (presidentId) REFERENCES USER(idUser) -- Associe un président
);


-- Table des événements
CREATE TABLE IF NOT EXISTS EVENEMENT_ORGANISE_PAR_ASSO (
    idEvent INT AUTO_INCREMENT PRIMARY KEY,
    shortCode VARCHAR(255) NOT NULL UNIQUE,
    idAsso INT NOT NULL,
    descriptionEvent TEXT,
    dateEvent DATETIME NOT NULL,
    FOREIGN KEY (idAsso) REFERENCES ASSOCIATION(idAsso)
);


GRANT SELECT, INSERT, UPDATE, DELETE ON assos.EVENEMENT_ORGANISE_PAR_ASSO TO 'president_username'@'%';



-- Create the news_db database and its tables
CREATE DATABASE IF NOT EXISTS news_db;

USE news_db;

CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);