import networkx as nx
import random

def generate_graph(num_nodes, probability, directed, graph_type, layout_type):
    if graph_type == 'Random':
        G = nx.fast_gnp_random_graph(num_nodes, probability, directed=directed)
    elif graph_type == 'Scale-free':
        G = nx.scale_free_graph(num_nodes)
        if not directed:
            G = G.to_undirected()
    elif graph_type == 'Small-world':
        G = nx.watts_strogatz_graph(num_nodes, 4, probability)
    
    # Determinar el layout
    if layout_type == 'Spring':
        pos = nx.spring_layout(G)
    elif layout_type == 'Circular':
        pos = nx.circular_layout(G)
    elif layout_type == 'Random':
        pos = nx.random_layout(G)
    elif layout_type == 'Shell':
        pos = nx.shell_layout(G)
    
    nx.set_node_attributes(G, pos, 'pos')
    
    return G