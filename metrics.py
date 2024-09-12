import networkx as nx
import streamlit as st
from community import community_louvain

def get_degree_metrics(G):
    if G.is_directed():
        in_degree = dict(G.in_degree())
        out_degree = dict(G.out_degree())
        return {node: (in_degree[node], out_degree[node]) for node in G.nodes()}
    else:
        return dict(G.degree())

def eigenvector_with_fallback(G):
    try:
        return nx.eigenvector_centrality(G, max_iter=1000, tol=1e-6)
    except nx.PowerIterationFailedConvergence:
        st.warning("Eigenvector centrality calculation failed to converge. Using degree centrality as a fallback.")
        return dict(nx.degree(G))
    
def graph_centroid(G):
    closeness = nx.closeness_centrality(G)
    return max(closeness, key=closeness.get)

def average_degree(G):
    return sum(dict(G.degree()).values()) / G.number_of_nodes()

def graph_density(G):
    return nx.density(G)

def connected_components(G):
    if G.is_directed():
        components = list(nx.weakly_connected_components(G))
    else:
        components = list(nx.connected_components(G))
    return {node: i for i, component in enumerate(components) for node in component}

metrics = {
    'Closeness': nx.closeness_centrality,
    'Betweenness': nx.betweenness_centrality,
    'Degree': get_degree_metrics,
    'Eigenvector': eigenvector_with_fallback,
    'PageRank': nx.pagerank,
    'Centroid': graph_centroid,
    'Edge Betweenness': nx.edge_betweenness_centrality,
    'Average Degree': average_degree,
    'Density': graph_density,
    'Connected Components': connected_components
}

def calculate_metric(G, metric_name):
    return metrics[metric_name](G)