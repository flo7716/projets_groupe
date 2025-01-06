-- Créer l'utilisateur pour la base de données assos avec le mot de passe
CREATE USER 'asso_scraper'@'%' IDENTIFIED BY '37867e0066c7214d';  -- Utilisez le mot de passe généré

-- Créer l'utilisateur pour la base de données news_db avec le mot de passe
CREATE USER 'news_scraper'@'%' IDENTIFIED BY 'cc62b1fad6b1061f';  -- Utilisez le mot de passe généré

-- Attribuer des droits uniquement à la base de données assos pour l'utilisateur asso_scraper
GRANT SELECT, INSERT, UPDATE, DELETE ON assos.* TO 'asso_scraper'@'%';

-- Attribuer des droits uniquement à la base de données news_db pour l'utilisateur news_scraper
GRANT SELECT, INSERT, UPDATE, DELETE ON news_db.* TO 'news_scraper'@'%';

-- Appliquer les changements de privilèges
FLUSH PRIVILEGES;
