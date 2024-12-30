import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import math
import time

ox.config(log_console=True)

# Load the graph of Stellenbosch
G = ox.graph_from_place("Stellenbosch, South Africa", network_type='drive')

# Convert the graph to undirected
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

# Create the reachability graph G_rt for different max distances
def create_reachability_graph(max_distance):
    G_rt = nx.Graph()
    G_rt.add_nodes_from(H.nodes)  # Ensure all nodes are added
    for node in H.nodes():
        reachable_nodes = modified_dijkstra(H, node, max_distance)
        for target, distance in reachable_nodes.items():
            if distance <= max_distance and node != target:
                G_rt.add_edge(node, target, weight=distance)
    return G_rt

# Randomized k-dominating set
def randomized_k_dominating_set(graph, k):
    delta = int(sum(dict(graph.degree()).values()) / len(graph.nodes()))
    delta_0 = delta - k + 1
    b_k_minus_1 = math.comb(delta, k - 1)
    p = 1 - 1 / (pow((b_k_minus_1 * (1 + delta_0)), (1 / delta_0)))

    A = set()
    for v in graph.nodes():
        if random.random() < p:
            A.add(v)
    while any(len(set(graph.neighbors(v)).intersection(A)) < k for v in graph.nodes() if v not in A):
        U = []
        for u in graph.nodes():
            if u not in A and len(set(graph.neighbors(u)).intersection(A)) < k:
                U.append(u)
        u = max((v for v in graph.nodes() if v not in A), key=lambda v: len(set(graph.neighbors(v)).intersection(U)))
        A.add(u)

    return A

# Check if D is a k-dominating set
def is_k_dominating(graph, D, k):
    for v in graph:
        if v not in D:
            count = sum(1 for neighbor in graph[v] if neighbor in D)
            if count < k:
                return False
    return True

# Minimize the k-dominating set
def minimal_k_dominating_set(graph, D, k):
    D = set(D)  # Convert to set if not already
    L = sorted(D, key=lambda v: len(set(graph[v]) - D))
    for v in L:
        if is_k_dominating(graph, D - {v}, k):
            D.remove(v)
    return D

# Iterate over max_distances and k values
for max_distance in [2000]:
    print(f"\nRunning simulation for max distance: {max_distance}")
    
    # Create the reachability graph G_rt for the current max_distance
    G_rt = nx.Graph()
    G_rt.add_nodes_from(H.nodes) 
    for node in H.nodes():
        reachable_nodes = modified_dijkstra(H, node, max_distance)
        for target, distance in reachable_nodes.items():
            if distance <= max_distance and node != target:
                G_rt.add_edge(node, target, weight=distance)
    
    # Run for k = 1, 2, 3
    for k in [1,2,3]:
        print(f"\nRunning for k = {k}")
        
        results = []
        combined = []
        count = 0



        start_time = time.time()
        k_dominating_set = randomized_k_dominating_set(G_rt, k)

        end_time = time.time()

        execution_time = end_time - start_time

        minimal_D = minimal_k_dominating_set(G_rt, k_dominating_set, k)
        min_time=time.time()

        ex_time=min_time-start_time
        results.append(len(minimal_D))
        combined.append(len(k_dominating_set))
        count += 1

        # Display the results
        print(f'For k = {k} and max distance = {max_distance}:')
        print('Lengths of combined k-dominating sets:', combined)
        print('Lengths of minimal dominating sets:', results)
        print('Execution time for greedy algorithm (in seconds):', execution_time)
        print('Execution time for greedy with minimal algorithm (in seconds):', ex_time)