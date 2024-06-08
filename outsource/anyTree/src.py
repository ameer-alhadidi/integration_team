import json
from anytree import Node, RenderTree

def create_tree(data):
    root = Node("Entity")

    for entity in data:
        entity_node = Node(entity["name"], parent=root)

        contacts_node = Node("Contacts", parent=entity_node)
        for contact in entity["contacts"]:
            contact_node = Node(contact["name"], parent=contacts_node)

        servers_node = Node("Servers", parent=entity_node)
        for server in entity["servers"]:
            server_node = Node(server["name"], parent=servers_node)
            ports_node = Node("Ports", parent=server_node)
            for port in server["ports"]:
                port_node = Node(f"Port {port['number']}", parent=ports_node)
                services_node = Node("Allowed Services", parent=port_node)
                for service in port["allowed_service"]:
                    service_node = Node(service["name"], parent=services_node)
                certificates_node = Node("Certificates", parent=port_node)
                for certificate in port["certificates"]:
                    certificate_node = Node(certificate["name"], parent=certificates_node)

        user_accounts_node = Node("User Accounts", parent=entity_node)
        for user in entity["user_accounts"]:
            user_node = Node(user["name"], parent=user_accounts_node)
            roles_node = Node("Roles", parent=user_node)
            for role in user["roles"]:
                role_node = Node(role, parent=roles_node)
            user_certificates_node = Node("Certificates", parent=user_node)
            for certificate in user["certificates"]:
                certificate_node = Node(certificate["name"], parent=user_certificates_node)

    return root

# Read JSON data from a file
with open("data.json") as file:
    json_data = json.load(file)

# Create the tree from JSON data
tree = create_tree(json_data)

# Print the tree
for pre, fill, node in RenderTree(tree):
    print(f"{pre}{node.name}")



from anytree.importer import JsonImporter

from anytree import RenderTree

j_string = '[{"name": "Bob", "languages": "English"}]'
importer = JsonImporter()
root = importer.import_(j_string)
print(RenderTree(root))
