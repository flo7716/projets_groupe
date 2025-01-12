# Documentation de l'API

## GET /api/associations
Retourne la liste de toutes les associations stockées dans DynamoDB.

**Réponse**:
```json
[
    {
        "id": 1,
        "name": "Association A",
        "description": "Description de l'association A"
    },
    ...
]


## Endpoints des Articles

### GET /api/articles
Retourne tous les articles.

#### Réponse
```json
{
  "message": "Articles récupérés avec succès!",
  "articles": [ ... ]
}
