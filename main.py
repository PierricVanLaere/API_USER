from fastapi import FastAPI, HTTPException, Depends
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

# Configurer le driver Neo4j
neo4j_uri = os.getenv("NEO4J_URI")  # ou l'adresse de ton serveur Neo4j
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

def get_neo4j_driver():
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    try:
        yield driver
    finally:
        driver.close()


@app.post("/create/user/{nom}/{prenom}")
async def create_user(nom: str, prenom: str, driver=Depends(get_neo4j_driver)):
    with driver.session() as session:
        try:
            query = """
            CREATE (u:User {nom: $nom, prenom: $prenom})
            RETURN u
            """
            result = session.run(query, nom=nom, prenom=prenom)
            user = result.single()
            return {"message": "Utilisateur créé avec succès", "user": {"nom": user["u"]["nom"], "prenom": user["u"]["prenom"]}}
        except Exception as e:
            return {"error": str(e)}