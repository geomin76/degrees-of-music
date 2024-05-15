import json
import pickle

data = {}
with open('./graph-data.json') as f:
    data = json.load(f)

graph = {}
for genre in data:
    graph[genre] = graph.get(genre, []) + data[genre]
    for inner_genre in data[genre]:
        graph[inner_genre] = graph.get(inner_genre, []) + [genre]

for genre in graph:
    cleanup_list = list(set(graph[genre]))
    if genre in cleanup_list:
        cleanup_list.remove(genre)
    graph[genre] = cleanup_list

dbfile = open('dataPickled', 'ab')
pickle.dump(graph, dbfile)                    
dbfile.close()