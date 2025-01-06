-- Générer des mots de passe aléatoires
SET @asso_password = SUBSTRING(MD5(RAND()), 1, 16);  -- Génère un mot de passe aléatoire de 16 caractères
SET @news_password = SUBSTRING(MD5(RAND()), 1, 16);  -- Génère un mot de passe aléatoire de 16 caractères

-- Créer l'utilisateur pour la base de données assos
CREATE USER 'asso_scraper'@'%' IDENTIFIED BY @asso_password;

-- Créer l'utilisateur pour la base de données news_db
CREATE USER 'news_scraper'@'%' IDENTIFIED BY @news_password;

-- Attribuer des droits uniquement à la base de données assos pour l'utilisateur asso_scraper
GRANT SELECT, INSERT, UPDATE, DELETE ON assos.* TO 'asso_scraper'@'%';

-- Attribuer des droits uniquement à la base de données news_db pour l'utilisateur news_scraper
GRANT SELECT, INSERT, UPDATE, DELETE ON news_db.* TO 'news_scraper'@'%';

-- Appliquer les changements de privilèges
FLUSH PRIVILEGES;

-- Afficher les mots de passe générés pour chaque utilisateur
SELECT @asso_password AS 'asso_scraper_password', @news_password AS 'news_scraper_password';