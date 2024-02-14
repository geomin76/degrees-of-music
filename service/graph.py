import json
from graph_client import Neo4JClient

data = {}
with open('./graph-data.json') as f:
    data = json.load(f)

neo4j = Neo4JClient()

genres = set()
for genre in data:
    genres.add(genre)
    for inner_genre in data[genre]:
        genres.add(inner_genre)

genres = list(genres)

def create_genre(tx, genre_name):
    query = (
        "CREATE (g1:Genre { name: $genre_name })"
    )
    result = tx.run(query, genre_name=genre_name)
    print(result)

def create_relationships(tx, genre_name_first, genre_name_second):
    query = (
        """
        MATCH (g1: Genre { name: $genre_name_first }),
              (g2: Genre { name: $genre_name_second })
        CREATE (g1)-[:`SIMILAR`]->(g2)
        """
    )
    result = tx.run(query, genre_name_first=genre_name_first, genre_name_second=genre_name_second)
    print(result)

count = 0
with neo4j.db().session(database="neo4j") as session: 
    for genre in genres:
         result = session.execute_write(create_genre, genre)
         count += 1
         print("Inserted data with count {}".format(count))

count = 0
with neo4j.db().session(database="neo4j") as session: 
    for genre in genres:
            visited = set()
            visited.add(genre)
            if genre in data:
                for similar_genre in data[genre]:
                    if similar_genre not in visited:
                        session.execute_write(create_relationships, genre, similar_genre)
                        visited.add(similar_genre)
                        count += 1
                        print("Inserted relationship with count {}".format(count))

neo4j.close()