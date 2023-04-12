from node import Node
from connection import Connection
import time

def load_circuit(file_path, is_considering_all=False):
    nodes_by_id = {}
    connections_by_id = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')

            try:
                node_id = int(parts[1])
            except ValueError:
                if not is_considering_all:
                    continue
                node_id = parts[1]

            nodes_by_id[node_id] = Node(node_id)

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')

            try:
                node_id = int(parts[1])
            except ValueError:
                if not is_considering_all:
                    continue
                node_id = parts[1]

            node_id_strings_list = parts[2].split(',')
            for node_id_string in node_id_strings_list:
                if node_id_string == '':
                    continue
                
                try:
                    sender_node_id = int(node_id_string)
                except ValueError:
                    if not is_considering_all:
                        continue
                    sender_node_id = node_id_string

                connections_by_id[len(connections_by_id)] = Connection(len(connections_by_id), sender_node_id, node_id)

    for connection in connections_by_id.values():
        nodes_by_id[connection.sender_node_id].connections.append(connection)
        nodes_by_id[connection.receiver_node_id].connections.append(connection)

    return nodes_by_id, connections_by_id

def load_circuit_groups(results_base_directory, file_name, nodes_by_id):
    groups = {}
    
    with open(f'{results_base_directory}nodes/{file_name}', 'r') as file:
        for i, line in enumerate(file):
            groups[i] = [nodes_by_id[int(node_id)] for node_id in line.split(',')]
    
    return groups

def save_circuit_groups(results_base_directory, groups, colours_used):
    resulting_max_num_gates_per_cell = max([len(group.node_ids) for group in groups])
    resulting_max_num_total_channels = len(set(colours_used.values()))

    base_file_name = f'max_nodes_{resulting_max_num_gates_per_cell}_max_channels_{resulting_max_num_total_channels}_num_cells_{len(groups)}_{int(time.time()*1000)}'

    with open(f'{results_base_directory}nodes/{base_file_name}', 'w') as file:
        for group in groups:
            file.write(','.join([str(node_id) for node_id in list(group.node_ids)]) + "\n")

    with open(f'{results_base_directory}channels/{base_file_name}', 'w') as file:
        file.write(str(colours_used))
