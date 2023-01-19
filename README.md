# Projet Webservice trains

## Lancement du projet

`docker-compose up`

URL de l'interface web: http://localhost:3000

## Architecture

- API REST : Python / FastAPI
- Base de données : PostgreSQL
- Serveur SOAP: Python / Spyne
- Client:
    - SOAP: Serveur Python / Zeep
    - Web:
        - Serveur Python / Pynecone
        - Front généré: NodeJS / React