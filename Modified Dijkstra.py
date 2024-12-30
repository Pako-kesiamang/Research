import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import heapq

# Configure osmnx
ox.config(log_console=True)

# Download and project the graph
G = ox.project_graph(ox.graph_from_place('Stellenbosch, South Africa', network_type='drive', which_result=1))

# Consolidate intersections
G2 = ox.consolidate_intersections(G, tolerance=1, rebuild_graph=True, dead_ends=True)

# Create a new graph with edge weights
H = nx.Graph(G2)
for u, v, data in G2.edges(data=True):
    if 'length' in data:
        H[u][v]['weight'] = data['length']

# Define the modified Dijkstra's algorithm
def modified_dijkstra(graph, initial_node, max_distance):
    reachable = set()
    heap = [(0, initial_node)]  # Priority queue
    distances = {initial_node: 0}

    while heap:
        (d, node) = heapq.heappop(heap)
        
        if d > max_distance:
            continue

        if node not in reachable:
            reachable.add(node)
        
        for neighbor, edge_data in graph[node].items():
            neighbor_dist = d + edge_data['weight']
            if neighbor_dist <= max_distance and (neighbor not in distances or neighbor_dist < distances[neighbor]):
                distances[neighbor] = neighbor_dist
                heapq.heappush(heap, (neighbor_dist, neighbor))

    return reachable

# Ensure initial node exists
initial_node = list(H.nodes())[0]  # Select the first node as the initial node
reachable_nodes = modified_dijkstra(H, initial_node, 1000)

# Find the neighbors of the initial node
neighbors = set(H.neighbors(initial_node))

# Plot the graph with the initial node blue, its neighbors red, and others black
node_colors = []
for node in H.nodes():
    if node == 0:
        node_colors.append('blue')
    elif node in reachable_nodes:
        node_colors.append('red')
    else:
        node_colors.append('black')

ox.plot_graph(G2, bgcolor="white", node_size=6, edge_linewidth=0.5, node_color=node_colors, show=True)



