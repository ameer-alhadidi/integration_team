import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import json

# Load data from JSON file
file = open("data.json", "r")
data = json.load(file)

def add_nodes_with_unique_identifiers_corrected(graph, data, parent_id=None, path="", show_properties=True):
    """ Recursively adds nodes and edges to the graph, with unique identifiers for each node based on their hierarchy path """
    for key, value in data.items():
        # Creating a unique path identifier for each node
        node_path = f"{path}/{value['key']}"

        if show_properties:
            # Node label includes the key and a summary of its properties
            node_label = f"{value['key']}\nChildren: {len(value['children'])}\nIsWord: {value.get('isWord', False)}"
        else:
            # Node label includes only the key
            node_label = f"{value['key']}"

        graph.add_node(node_path, label=node_label)

        if parent_id is not None:
            graph.add_edge(parent_id, node_path)
        
        if 'children' in value and value['children']:
            add_nodes_with_unique_identifiers_corrected(graph, value['children'], node_path, node_path, show_properties)

# Option to show properties in the node labels
show_node_properties = False  # Set to False to hide properties

# Creating a new directed graph for the representation with corrected unique identifiers
G_with_correct_unique_ids = nx.DiGraph()

# Adding a null root node with optional properties
root_id = "/null"
root_label = "ROOT\nnull\nChildren: 1\nIsWord: False" if show_node_properties else "ROOT\nnull"
G_with_correct_unique_ids.add_node(root_id, label=root_label)

# Adding other nodes with optional properties and corrected unique identifiers
add_nodes_with_unique_identifiers_corrected(G_with_correct_unique_ids, data['children'], parent_id=root_id, show_properties=show_node_properties)

# Plotting the tree with optional properties and corrected unique identifiers
plt.figure(figsize=(12, 8))
pos = graphviz_layout(G_with_correct_unique_ids, prog='dot')
nx.draw(G_with_correct_unique_ids, pos, with_labels=True, labels=nx.get_node_attributes(G_with_correct_unique_ids, 'label'), 
        arrows=True, node_size=3000, node_color="lightblue", font_size=10)
plt.title("Tree Diagram with Corrected Unique Node Identifiers", size=15)
plt.show()
