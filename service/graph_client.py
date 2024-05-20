import random
import pickle
from dotenv import load_dotenv
load_dotenv()

dbfile = open('dataPickled', 'rb')    
graph = pickle.load(dbfile)
dbfile.close()

def bfs(genres, depth):
    d = {}
    for genre in genres:
        path = []
        path.append(genre)
        returned_genre = bfs_helper(genre, depth, path)
        d[genre] = {
            "returned_genre": returned_genre,
            "path": path
        }
    
    return d

def bfs_helper(genre, depth, paths):
    for _ in range(depth):
        if graph.get(genre):
            returned_genres = graph[genre]
            for inner_genre in returned_genres:
                if inner_genre in paths:
                    returned_genres = [i for i in returned_genres if i != inner_genre]
            if len(returned_genres) == 0:
                return genre
            genre = random.choices(returned_genres, k = 1)[0]
            paths.append(genre)
    return genre

