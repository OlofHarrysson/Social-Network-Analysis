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
    # casts = casts[:2000] # Runs in about 2 minutes
    # casts = casts[:6000] # Runs in about 15 minutes

    movies_dict = dict()
    actor_names = []
    for line in casts:
        line = line.split(';')
        actor = line[2].replace('"', '')
        movie = line[1].replace('"', '')

        if actor == "" or actor == "s a" or movie == "":
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


def create_kevin_bacon(G):
    nodes = G.nodes()
    nodes.remove('Kevin Bacon')

    kevin_bacon = []

    for n in nodes:
        try:
            path = nx.shortest_path(G, n, 'Kevin Bacon')
            del path[0]
            kevin_bacon.append((n, len(path)))
        except:
            continue

    return kevin_bacon


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

clusters = nx.clustering(G)


print("n_nodes = " + str(n_nodes))
print("n_edges = " + str(n_edges))
print("density = " + str(density))
print("number of components = " + str(n_components))


top_degree = sorted(degree_centrality, key=lambda x: x[1], reverse=True)[:5]
print("\ntop {:d} with degree centrality = {:s}\n".format(len(top_degree), str(top_degree)))

top_closeness = sorted(closeness_centrality, key=lambda x: x[1])[:5]
print("top {:d} with closeness centrality = {:s}\n".format(len(top_closeness), str(top_closeness)))

top_between = sorted(betweeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("top {:d} with between centrality = {:s}\n".format(len(top_between), str(top_between)))

top_clusters = sorted(clusters.items(), key=lambda x: x[1], reverse=True)[:5]
print("top {:d} cluster nodes = {:s}\n".format(len(top_clusters), str(top_clusters)))


kevin_bacon = create_kevin_bacon(G)
bottom_kevin = sorted(kevin_bacon, key=lambda x: x[1], reverse=False)[:5]
top_kevin = sorted(kevin_bacon, key=lambda x: x[1], reverse=True)[:5]
avg_kevin_bacon = sum(a[1] for a in kevin_bacon) / len(kevin_bacon)
print("The nodes closes to Kevin bacon = {:s}\n".format(str(bottom_kevin)))
print("The nodes furthest away to Kevin bacon = {:s}\n".format(str(top_kevin)))
print("The average degree of seperation to Kevin Bacon is = {:f}\n".format(avg_kevin_bacon))

for node, value in top_degree:
    nx.set_node_attributes(G, 'Top Degree Centrality', {node: value})

for node, value in top_closeness:
    nx.set_node_attributes(G, 'Top Closeness Centrality', {node: value})

for node, value in top_between:
    nx.set_node_attributes(G, 'Top Betweeness Centrality', {node: value})

for node, value in top_clusters:
    nx.set_node_attributes(G, 'Top Clusters', {node: value})

for node, value in bottom_kevin:
    nx.set_node_attributes(G, 'Closest to Kevin Bacon', {node: value})

for node, value in top_kevin:
    nx.set_node_attributes(G, 'Furthest away from Kevin Bacon', {node: value})


nodes = G.nodes()
max_edges = top_degree[0][1]
max_size = 110
size_values = []

for n in nodes:
    n_edges = nx.edges(G, nbunch=n)
    rel_edge = len(n_edges) / max_edges
    if rel_edge > 0.5:
        size_values.append(rel_edge * rel_edge * max_size)
    else:
        size_values.append(20)

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=range(len(nodes)),node_size=30,cmap=plt.cm.Vega20b)
nx.draw_networkx_edges(G, pos, width=0.5)
plt.show()

nx.draw_networkx_nodes(G, pos, node_color=range(len(nodes)),node_size=size_values,cmap=plt.cm.Vega20b)
nx.draw_networkx_edges(G, pos, width=0.5)
plt.show()

nx.write_gexf(G, 'graph.gexf')
