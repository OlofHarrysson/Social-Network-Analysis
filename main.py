import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt
from collections import defaultdict


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
    casts = casts[:300] # Shorten the data due to time issues

    movies_dict = dict()
    actor_names = []
    for line in casts:
        line = line.split(';')
        actor = line[2].replace('"', '')
        movie = line[1].replace('"', '')

        if actor == "" or movie == "":
            continue

        actor_names.append(actor)
        try:
            movies_dict[movie].append(actor)
        except KeyError:
            movies_dict[movie] = [actor]


    actor_names = set(actor_names)

    actors = dict()
    for name in actor_names:
        actors[name] = Actor(name)

    for movie, actor_names in movies_dict.items():
        create_edges(actor_names, actors)

    return actors

def create_closeness(G):
    nodes = G.nodes()
    n_nodes = len(nodes)
    betweeness_centrality = defaultdict(int)

    nodes_avg_l = []
    for n1 in nodes:
        avg_l = 0
        n_unconnected = 1 # Always unconnected to itself

        for n2 in nodes:
            if n1 != n2:
                try:
                    path = nx.shortest_path(G, n1, n2)
                    del path[0]
                    avg_l += len(path)

                    for p in path:
                        betweeness_centrality[p] += 1
                except:
                    n_unconnected += 1

        if n_nodes - n_unconnected == 0:
            continue # Node is unconnected
        else:
            nodes_avg_l.append((n1, avg_l / (n_nodes - n_unconnected)))


    return nodes_avg_l, betweeness_centrality


#################################### START ####################################

actors = create_graph() # Dict where key = name, value = obj
n_nodes = len(actors)
n_edges = 0


G = nx.Graph() # Graph where node = name, edge = name
for node_name, a in actors.items():
    n_edges += len(a.edges)
    for edge_name, edge in a.edges.items():
        G.add_edge(node_name, edge_name)

density = n_edges / (n_nodes * (n_nodes - 1))
n_components = nx.number_connected_components(G)


degree_centrality = [(name, len(a.edges)) for name, a in actors.items()]

closeness_centrality, betweeness_centrality = create_closeness(G)

