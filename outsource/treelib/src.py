import json
from treelib import Node, Tree
from graphviz import Digraph

# Load the JSON data
with open('data.json') as file:
    data = json.load(file)

# Create a new tree
tree = Tree()

# Traverse the JSON data and build the tree
for entity in data:
    entity_id = entity['id']
    entity_name = entity['name']
    entity_abbr = entity['ABBR']

    # Add the entity as the root node
    tree.create_node(f"{entity_name} ({entity_abbr})", entity_id)

    # Add contacts as child nodes
    for contact in entity['contacts']:
        contact_id = contact['id']
        contact_name = contact['name']
        contact_email = contact['email']
        contact_number = contact['number']
        tree.create_node(f"{contact_name}\nEmail: {contact_email}\nNumber: {contact_number}", contact_id, parent=entity_id)

    # Add servers as child nodes
    for server in entity['servers']:
        server_id = server['id']
        server_name = server['name']
        server_ip = server['ip_address']
        server_status = server['status']
        tree.create_node(f"{server_name}\nIP: {server_ip}\nStatus: {server_status}", server_id, parent=entity_id)

        # Add ports as child nodes
        for port in server['ports']:
            port_id = port['id']
            port_number = port['number']
            tree.create_node(f"Port {port_number}", port_id, parent=server_id)

            # Add allowed services as child nodes
            for service in port['allowed_service']:
                service_id = service['id']
                service_name = service['name']
                tree.create_node(service_name, service_id, parent=port_id)

            # Add certificates as child nodes
            for cert in port['certificates']:
                cert_id = cert['id']
                cert_name = cert['name']
                cert_expiry = cert['expiry_date']
                tree.create_node(f"{cert_name}\nExpires: {cert_expiry}", cert_id, parent=port_id)

    # Add user accounts as child nodes
    for user in entity['user_accounts']:
        user_name = user['name']
        user_roles = ', '.join(user['roles'])
        tree.create_node(f"{user_name}\nRoles: {user_roles}", user_name, parent=entity_id)

        # Add user certificates as child nodes
        for cert in user['certificates']:
            cert_name = cert['name']
            cert_expiry = cert['expiry_date']
            tree.create_node(f"{cert_name}\nExpires: {cert_expiry}", cert_name, parent=user_name)

# Create a Graphviz Digraph object
graph = Digraph()

# Recursively add nodes and edges to the graph
def add_nodes_and_edges(node):
    graph.node(str(node.identifier), label=node.tag.replace('\n', '\\n'))
    for child in tree.children(node.identifier):
        add_nodes_and_edges(child)
        graph.edge(str(node.identifier), str(child.identifier))

# Add nodes and edges to the graph
add_nodes_and_edges(tree.get_node(tree.root))

# Save the graph as a PNG image
graph.render('tree_output', format='png', cleanup=True)