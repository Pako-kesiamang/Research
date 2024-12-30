import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random

# Configure osmnx
ox.config(log_console=True)

G = ox.graph_from_place("Stellenbosch, South Africa", network_type='drive')

G = G.to_undirected()

H = nx.Graph(G)
for u, v, data in G.edges(data=True):
    if 'length' in data:
        H[u][v]['weight'] = data['length']

def modified_dijkstra(graph, initial_node, max_distance):
    reachable = {}
    heap = [(0, initial_node)]  

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

# Create the reachability graph Grt

G_rt = nx.Graph()
max_distance = 1000
k = 2


for node in H.nodes():
    reachable_nodes = modified_dijkstra(H, node, max_distance)
    for target, distance in reachable_nodes.items():
        if distance <= max_distance and node != target:
            G_rt.add_edge(node, target, weight=distance)

#Greedy algorithm
def greedy_k_dominating_set(G, k, D):
    while any(len(set(G.neighbors(v)).intersection(D)) < k for v in G.nodes() if v not in D):
        U = []
        for u in G.nodes():
            if u not in D and len(set(G.neighbors(u)).intersection(D)) < k:
                U.append(u)
        u = max((v for v in G.nodes() if v not in D), key=lambda v: len(set(G.neighbors(v)).intersection(U)))
        D.add(u)
    return D
#minimal k-dominating set
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

for i in range(10):
    # Start with an empty dominating set D or any initial node
    D = {list(G.nodes())[random.randint(0, len(G.nodes()) - 1)]} # Start with a random node
    
    # Find the k-dominating set
    k_dominating_set = greedy_k_dominating_set(G_rt, k, D)
    minimal_D=minimal_k_dominating_set(G_rt,k_dominating_set, k)
    results.append(len(minimal_D))
    combined.append(len(k_dominating_set))


# Display the results
print('Lengths of combined k-dominating sets:', combined)
print('Lengths of combined dominating sets:', sum(combined)/10)
print('Lengths of minimal dominating sets:', results)
print('Lengths of minimal dominating sets:', sum(results)/10)