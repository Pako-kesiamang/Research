import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import math 


ox.config(log_console=True)

G = ox.graph_from_place("Stellenbosch, South Africa", network_type='drive')

G = G.to_undirected()

# Create a new graph with edge weights
H = nx.Graph()
for u, v, data in G.edges(data=True):
    if 'length' in data:
        H.add_edge(u, v, weight=data['length'])

# Define the modified Dijkstra's algorithm
def modified_dijkstra(graph, initial_node, max_distance):
    reachable = {}
    heap = [(0, initial_node)]  # Priority queue

    while heap:
        (d, node) = heapq.heappop(heap)
        if node not in reachable:
            reachable[node] = d

        if d > max_distance:
            continue

        for neighbor, edge_data in graph[node].items():
            neighbor_dist = d + edge_data['weight']
            if neighbor not in reachable and neighbor_dist <= max_distance:
                heapq.heappush(heap, (neighbor_dist, neighbor))

    return reachable

# Create the reachability graph G_rt
G_rt = nx.Graph()
max_distance = 3000  # 1 km
k = 3
for node in H.nodes():
    reachable_nodes = modified_dijkstra(H, node, max_distance)
    for target, distance in reachable_nodes.items():
        if distance <= max_distance and node != target:
            G_rt.add_edge(node, target, weight=distance)

print("Number of nodes in G_rt:", G_rt.number_of_nodes())
print("Number of edges in G_rt:", G_rt.number_of_edges())

print("Number of nodes in G:", G.number_of_nodes())
print("Number of edges in G:", G_rt.number_of_edges())

def randomized_k_dominating_set(graph, k):
    delta = int(sum(dict(graph.degree()).values())/len(graph.nodes()))
    print('delta:', delta)
    delta_0 = delta - k + 1
    b_k_minus_1 = math.comb(delta, k - 1)
    p = 1 - 1 / (pow((b_k_minus_1 * (1 + delta_0)), (1 / delta_0)))
    print('Probability:', p)

    A = set()
    for v in graph.nodes():
        if random.random() < p:
            A.add(v)

    B = set()
    for v in graph.nodes():
        if v not in A:
            if len(set(graph.neighbors(v)).intersection(A)) < k:
                B.add(v)

    D = A.union(B)

    return D

def is_k_dominating(graph, D, k):
    for v in graph:
        if v not in D:
            count = sum(1 for neighbor in graph[v] if neighbor in D)
            if count < k:
                return False
    return True

def minimal_k_dominating_set(graph, D, k):
    D = set(D)  # Convert to set if not already
    L = sorted(D, key=lambda v: len(set(graph[v]) - D))
    for v in L:
        if is_k_dominating(graph, D - {v}, k):
            D.remove(v)
    return D

results = []
combined=[]
count = 0

while count < 1:
    k_dominating_set = randomized_k_dominating_set(G_rt, k)
    minimal_D = minimal_k_dominating_set(G_rt, k_dominating_set, k)
    results.append(len(minimal_D))
    combined.append(len(k_dominating_set))
    count += 1

# Display the results
print('Lengths of combined k-dominating sets:', combined)
print('Lengths of combined dominating sets:', sum(combined)/10)
print('Lengths of minimal dominating sets:', results)
print('Lengths of minimal dominating sets:', sum(results)/10)
# Compute k-dominating set
# k_dominating_set = randomized_k_dominating_set(G_rt, k)

# node_colors = ['red' if node in k_dominating_set else 'black' for node in G.nodes()]

# # Use OSMnx to plot the graph with highlighted nodes
# fig, ax = ox.plot_graph(G, node_size=6, node_color=node_colors, edge_color='grey', bgcolor='white', show=False, close=False)
# plt.title("Graph of Stellenbosch with 2-Dominating Set Highlighted")
# plt.show()

# minimal_D = minimal_k_dominating_set(G_rt, k_dominating_set, k)
# print('minimal=', len(minimal_D))
# node_colors = ['red' if node in minimal_D else 'black' for node in G.nodes()]

# # Use OSMnx to plot the graph with highlighted nodes
# fig, ax = ox.plot_graph(G, node_size=6, node_color=node_colors, edge_color='grey', bgcolor='white', show=False, close=False)
# plt.title("Graph of Stellenbosch with 2-Dominating Set Highlighted")
# plt.show()