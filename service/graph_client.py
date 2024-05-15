import random
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

dbfile = open('dataPickled', 'rb')    
graph = pickle.load(dbfile)
dbfile.close()

def bfs(genres, depth):
    for _ in range(depth):
        new_genres = set()
        for genre in set(genres):
            if graph.get(genre):
                returned_genres = graph[genre]
                new_genres.update([returned_genre for returned_genre in returned_genres if returned_genre not in genres and returned_genre != genre])
        genres = new_genres
    return random.choices(list(genres), k = 15)


