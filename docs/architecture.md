# Architecture du projet

Ce projet est une application web permettant de gérer des associations. Il est composé d'un backend en **Flask**, d'un frontend en **HTML/CSS/JS**, et d'une base de données **AWS DynamoDB**.

## Backend (Flask)
- Flask est utilisé pour gérer les routes et la logique serveur.
- DynamoDB est utilisé comme base de données NoSQL pour stocker et récupérer les données des associations.

## Frontend
- HTML est utilisé pour la structure des pages.
- CSS est utilisé pour le style.
- JavaScript permet d'interagir avec l'API.

## Docker
Le projet peut être exécuté dans un conteneur Docker, facilitant son déploiement et son exécution.

## DynamoDB
Les données des associations sont stockées dans une table DynamoDB. L'ID des associations est utilisé comme clé primaire.

## API
L'API expose les données des associations sous forme JSON.
