import colorsys
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import streamlit as st

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7 + random.random() * 0.3
        lightness = 0.4 + random.random() * 0.2
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append(f'rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})')
    return colors


def visualize_graph(G, metric, metric_option, directed_graph, graph_type):
    net = Network(notebook=True, directed=directed_graph)
    # Añadir información general del grafo si es necesario
    graph_info = ""
    if metric_option == 'Connected Components':
        unique_components = set(metric.values())
        color_map = {comp: color for comp, color in zip(unique_components, generate_distinct_colors(len(unique_components)))}
        num_components = len(unique_components)
        graph_info = f"Number of Connected Components: {num_components}"
    if metric_option in ['Average Degree', 'Density']:
        graph_info = f"{metric_option}: {metric:.2f}"
    
    for node in G.nodes:
        if metric_option == 'Connected Components':
            label = f'Node {node}\nComponent: {metric[node]}'
            
        elif directed_graph and metric_option == 'Degree' and graph_type != 'Small-world':
            label = f'Node {node}\nIn-degree: {metric[node][0]}\nOut-degree: {metric[node][1]}'
        elif metric_option == 'Centroid':
            label = f'Node {node}\n{"Centroid" if node == metric else ""}'
        elif metric_option in ['Edge Betweenness', 'Average Degree', 'Density']:
            label = f'Node {node}'   
        else:
            label = f'Node {node}\n{metric_option}: {metric[node]:.2f}' if isinstance(metric[node], float) else f'Node {node}\n{metric_option}: {metric[node]}'
  
        if metric_option == 'Connected Components':
            color = color_map[metric[node]]
        else:   
            color = 'red' if node == metric and metric_option == 'Centroid' else 'gray'
        net.add_node(node, label=label, shape='dot', title=label, color=color)
    
    for edge in G.edges:
            if metric_option == 'Edge Betweenness':
                # Para Edge Betweenness, mostramos el valor en las aristas
                edge_value = metric.get(edge, metric.get((edge[1], edge[0])))  # Maneja grafos no dirigidos
                title = f'Edge Betweenness: {edge_value:.2f}'
                net.add_edge(edge[0], edge[1], title=title, label=f'{edge_value:.2f}')
            else:
                net.add_edge(edge[0], edge[1])

    if graph_info:
        st.write(graph_info)         
        
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_file.seek(0)
        HtmlFile = tmp_file.read().decode('utf-8')

    components.html(HtmlFile, height=600)