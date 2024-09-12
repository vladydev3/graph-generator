import streamlit as st

def create_sidebar():
    directed_graph = st.sidebar.checkbox('Directed graph')
    probability = st.sidebar.slider('Probability of edge by node', 0.0, 1.0, 0.1)
    num_nodes = st.sidebar.slider('Number of nodes', 1, 50)

    graph_type = st.sidebar.selectbox('Graph type', ['Random', 'Scale-free', 'Small-world'])
    
    # Opción para layout
    layout_type = st.sidebar.selectbox('Layout', ['Spring', 'Circular', 'Random', 'Shell'])
    
    return directed_graph, probability, num_nodes, graph_type, layout_type

def create_metric_selector():
    options = [
        'Closeness', 
        'Betweenness', 
        'Degree', 
        'Eigenvector',
        'PageRank',
        'Centroid',
        'Edge Betweenness',
        'Average Degree',
        'Density',
        'Connected Components'
    ]
    option = st.selectbox('Metrics: ', options, key='metric_selector')
    return option