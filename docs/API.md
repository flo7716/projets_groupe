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


---

### Résumé :

Les scripts et la documentation ont été réécrits pour utiliser AWS DynamoDB dans l'application Flask. La structure de l'application reste inchangée, et les requêtes vers la base de données ont été adaptées pour utiliser DynamoDB via le SDK **Boto3**.
