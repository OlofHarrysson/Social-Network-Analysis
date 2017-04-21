import numpy as np
import networkx as nx


def read_file(path): # Splits at blank space
    file = open(path, 'r')
    return file.read().split('\n')

class Actor():
    def __init__(self, name):
        self.name = name
        self.edges = dict()

    def set_edge(self, actor):
        self.edges[actor.name] = actor

    def __str__(self):  # TODO edges
        return "Name is {:s}. Nbr of edges is {:d}".format(self.name, len(self.edges))

def create_edges(actor_names, actors):
    actors_in_movie = [actors[name] for name in actor_names]

    for i in range(len(actors_in_movie)):
        for j in range(i+1, len(actors_in_movie)):
            a1 = actors_in_movie[i]
            a2 = actors_in_movie[j]

            a1.set_edge(a2)
            a2.set_edge(a1)

def create_graph():
    casts = read_file('casts.csv')

    movies_dict = dict()
    actors_temp = []
    for line in casts:
        line = line.split(';')
        actor = line[2].replace('"', '')
        movie = line[1].replace('"', '')
        actors_temp.append(actor)

        try:
            movies_dict[movie].append(actor)
        except KeyError:
            movies_dict[movie] = [actor]


    actors_temp = set(actors_temp)

    actors = dict()
    for actor in actors_temp:
        actors[actor] = Actor(actor)

    for movie, actor_names in movies_dict.items():
        create_edges(actor_names, actors)

    G = nx.Graph()
    G.add_nodes_from(actors)

#################################### START ####################################

actors = create_graph()

degree_centrality = [(name, len(a.edges)) for name, a in actors.items()]

# TODO: Closeness centrality

# TODO: Betweeness Centrality



# print(movies_dict)
