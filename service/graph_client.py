import random
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

class Neo4JClient:
    def __init__(self):
        self.database = GraphDatabase.driver(DB_URI, auth=(DB_USERNAME, DB_PASSWORD))

    def db(self):
        return self.database

    def close(self):
        self.database.close()

def query(tx, genre):
    query = (
        """
        MATCH (g1: Genre { name: $genre_name })
        MATCH (g1)-[r]-(g2)
        RETURN g2.name
        """
    )
    results = tx.run(query, genre_name=genre)
    genres = []
    for result in set(results):
        genres.append(result.data()["g2.name"])
    
    return genres

def search_graph(neo4j, genre):
    with neo4j.db().session(database="neo4j") as session:
        returned_genres = set()
        returned_genres.update(session.execute_read(query, genre))
        return list(returned_genres)

def bfs(genres, depth):
    neo4j = Neo4JClient()
    for _ in range(depth):
        new_genres = set()
        for genre in set(genres):
            returned_genres = search_graph(neo4j, genre)
            new_genres.update([returned_genre for returned_genre in returned_genres if returned_genre not in genres and returned_genre != genre])
        genres = new_genres
    neo4j.close()
    return random.choices(list(genres), k = 15)

