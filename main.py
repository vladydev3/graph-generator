import streamlit as st
from ui_components import create_sidebar, create_metric_selector
from graph_generator import generate_graph
from metrics import calculate_metric
from visualization import visualize_graph

def main():
    st.title('Graph Generator')
    st.write('This is a simple web app that generates a random graph.')

    directed_graph, probability, num_nodes, graph_type, layout_type = create_sidebar()
    metric_option = create_metric_selector()

    G = generate_graph(num_nodes, probability, directed_graph, graph_type, layout_type)
    metric = calculate_metric(G, metric_option)
    visualize_graph(G, metric, metric_option, directed_graph, graph_type)


if __name__ == "__main__":
    main()