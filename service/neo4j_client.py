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