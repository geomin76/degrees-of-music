from neo4j_client import Neo4JClient

neo4j = Neo4JClient()

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

def search_graph(genre):
    with neo4j.db().session(database="neo4j") as session:
        returned_genres = set()
        print("Getting data for {}".format(genre))
        returned_genres.update(session.execute_read(query, genre))
        return list(returned_genres)

def bfs(genres, depth):
    for _ in range(depth):
        new_genres = set()
        for genre in set(genres):
            returned_genres = search_graph(genre)
            new_genres.update([returned_genre for returned_genre in returned_genres if returned_genre not in genres and returned_genre != genre])
        genres = new_genres
    
    return genres

"""
TODO:
obviously, the BFS can get out of hand. So it might be good to randomly pick data to a smaller subset in order to not overload Spotify API
"""
genres = ["orchestral soundtrack","soundtrack", "alternative hip hop", "modern rock", "rock", "french soundtrack", "orchestral soundtrack", "soundtrack", "anime", "anime score", "japanese classical", "japanese soundtrack", "orchestral soundtrack","german soundtrack", "orchestral soundtrack", "soundtrack"]
print(bfs(genres, 2))