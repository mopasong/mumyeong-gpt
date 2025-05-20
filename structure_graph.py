import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
import os

def draw_structure_graph(user_log):
    G = nx.DiGraph()

    # Define simple rules for demonstration
    for i, entry in enumerate(user_log):
        text = entry["text"]
        node_label = f"{i+1}. {text[:10]}..."
        G.add_node(node_label)

        if i > 0:
            prev_text = user_log[i-1]["text"]
            prev_label = f"{i}. {prev_text[:10]}..."
            G.add_edge(prev_label, node_label)

    net = Network(height='450px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(G)
    path = "/tmp/mumyeong_graph.html"
    net.save_graph(path)
    with open(path, "r", encoding="utf-8") as f:
        graph_html = f.read()
    components.html(graph_html, height=480, scrolling=True)