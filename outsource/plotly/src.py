import json
import networkx as nx
from plotly.graph_objs import *
from plotly.offline import plot

# Load JSON data from a file
with open('data.json') as file:
    data = json.load(file)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges from the JSON data
for entity in data:
    entity_id = entity['id']
    entity_name = entity['name']
    G.add_node(entity_id, name=entity_name, node_type='entity')

    for contact in entity['contacts']:
        contact_id = contact['id']
        contact_name = contact['name']
        G.add_node(contact_id, name=contact_name, node_type='contact')
        G.add_edge(entity_id, contact_id, edge_type='has_contact')

    for server in entity['servers']:
        server_id = server['id']
        server_name = server['name']
        G.add_node(server_id, name=server_name, node_type='server')
        G.add_edge(entity_id, server_id, edge_type='has_server')

        for port in server['ports']:
            port_id = port['id']
            port_number = port['number']
            G.add_node(port_id, name=port_number, node_type='port')
            G.add_edge(server_id, port_id, edge_type='has_port')

            for service in port['allowed_service']:
                service_id = service['id']
                service_name = service['name']
                G.add_node(service_id, name=service_name, node_type='service')
                G.add_edge(port_id, service_id, edge_type='allows_service')

            for certificate in port['certificates']:
                certificate_id = certificate['id']
                certificate_name = certificate['name']
                G.add_node(certificate_id, name=certificate_name, node_type='certificate')
                G.add_edge(port_id, certificate_id, edge_type='has_certificate')

    for user in entity['user_accounts']:
        user_name = user['name']
        G.add_node(user_name, name=user_name, node_type='user')
        G.add_edge(entity_id, user_name, edge_type='has_user')

        for role in user['roles']:
            G.add_node(role, name=role, node_type='role')
            G.add_edge(user_name, role, edge_type='has_role')

        for certificate in user['certificates']:
            certificate_name = certificate['name']
            G.add_node(certificate_name, name=certificate_name, node_type='certificate')
            G.add_edge(user_name, certificate_name, edge_type='has_certificate')

# Get the positions of the nodes for visualization
pos = nx.spring_layout(G)

# Create a list of edges with corresponding positions
edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

# Create a list of nodes with corresponding positions and labels
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        line=dict(width=2)
    )
)

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([G.nodes[node]['name']])

# Create the figure
fig = Figure(data=[edge_trace, node_trace],
             layout=Layout(
                title='Interactive Graph Visualization',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
             )
            )

# Plot the graph
plot(fig, filename='interactive_graph.html')