import random
import time
import copy
from collections import defaultdict

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.connections = []
        
    def __str__(self):
        return f'Node: id – {self.id}, connections – {[connection.get_simple_string() for connection in self.connections]}'

class Connection:
    def __init__(self, connection_id, sender_node_id, receiver_node_id):
        self.id = connection_id
        self.sender_node_id = sender_node_id
        self.receiver_node_id = receiver_node_id
        self.channel_id = self.sender_node_id
        
    def get_simple_string(self):
        return f'({self.sender_node_id}-{self.receiver_node_id})'
        
    def __str__(self):
        return f'Connection: id – {self.id}, sender_node_id-receiver_node_id – {get_simple_string()}'

class Group:
    def __init__(self, group_id):
        self.id = group_id
        self.node_ids = set()
        self.connection_count_by_external_node_ids = defaultdict(int)
        self.endpoint_count_by_channel_id = defaultdict(int)
        
    def __str__(self):
        return f'Group: id – {self.id}, node_ids – {self.node_ids}'

def main(max_nodes_per_group, max_channels_total):
    # SETUP
    connections_by_id = {}
    nodes_by_id = {}

    with open('circuit.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(';')

            try:
                node_id = int(parts[1])
            except ValueError:
                continue

            nodes_by_id[node_id] = Node(node_id)

    with open('circuit.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(';')

            try:
                node_id = int(parts[1])
            except ValueError:
                continue

            node_id_strings_list = parts[2].split(',')
            for node_id_string in node_id_strings_list:
                try:
                    sender_node_id = int(node_id_string)
                except ValueError:
                    continue

                connections_by_id[len(connections_by_id)] = Connection(len(connections_by_id), sender_node_id, node_id)
            
    for connection in connections_by_id.values():
        nodes_by_id[connection.sender_node_id].connections.append(connection)
        nodes_by_id[connection.receiver_node_id].connections.append(connection)


    connection_count_by_node_id = defaultdict(int)
    node_id_by_connection_count = defaultdict(set)

    for connection in connections_by_id.values():
        connection_count_by_node_id[connection.sender_node_id] += 1
        connection_count_by_node_id[connection.receiver_node_id] += 1

    for node_id, connection_count in connection_count_by_node_id.items():
        node_id_by_connection_count[connection_count].add(node_id)

    connection_count_by_node_id = dict(connection_count_by_node_id)    
    node_id_by_connection_count = dict(node_id_by_connection_count)

    connected_node_ids_by_node_id = defaultdict(set)

    for connection in connections_by_id.values():
        connected_node_ids_by_node_id[connection.sender_node_id].add(connection.receiver_node_id)
        connected_node_ids_by_node_id[connection.receiver_node_id].add(connection.sender_node_id)

    connected_node_ids_by_node_id = dict(connected_node_ids_by_node_id)

    endpoint_count_by_channel_id = defaultdict(int)

    for connection in connections_by_id.values():
        endpoint_count_by_channel_id[connection.channel_id] += 2

    endpoint_count_by_channel_id = dict(endpoint_count_by_channel_id)

    channel_ids_by_node_id = defaultdict(set)

    for connection in connections_by_id.values():
        channel_ids_by_node_id[connection.sender_node_id].add(connection.channel_id)
        channel_ids_by_node_id[connection.receiver_node_id].add(connection.channel_id)

    channel_ids_by_node_id = dict(channel_ids_by_node_id)
    
    
    
    
    # RUN
    groups_by_id = {}
    node_ids_all = set(nodes_by_id.keys())
    node_ids_claimed = set()
    max_connection_count = max(node_id_by_connection_count)

    def get_random_id_from_set(id_set):
        return random.choice(
            tuple(
                id_set
            )
        )

    def get_unclaimed_min_connection_nodes():
        node_ids = set()
        curr_min_num_connections = min(node_id_by_connection_count)

        while len(node_ids) <= 0:
            node_ids = node_id_by_connection_count[curr_min_num_connections] - node_ids_claimed
            curr_min_num_connections += 1

        return node_ids

    def claim_node_id_for_group(group, node_id):
        node_ids_claimed.add(node_id)
        add_node_id_to_group(group, node_id)

    def add_node_id_to_group(group, node_id):
        group.node_ids.add(node_id)

        for channel_id in channel_ids_by_node_id[node_id]:
            group.endpoint_count_by_channel_id[channel_id] += 1

        for connected_node_id in connected_node_ids_by_node_id[node_id]:
            group.connection_count_by_external_node_ids[connected_node_id] += 1

    def disclaim_node_id_for_group(group, node_id):
        node_ids_claimed.remove(node_id)
        remove_node_id_from_group(group, node_id)

    def remove_node_id_from_group(group, node_id):
        group.node_ids.remove(node_id)

        for channel_id in channel_ids_by_node_id[node_id]:
            group.endpoint_count_by_channel_id[channel_id] -= 1

        removed_channel_ids = []
        for channel_id, endpoint_count in group.endpoint_count_by_channel_id.items():
            if endpoint_count <= 0:
                removed_channel_ids.append(channel_id)

        for removed_channel_id in removed_channel_ids:
            group.endpoint_count_by_channel_id.pop(removed_channel_id)

        removed_connected_node_ids = []    
        for external_node_id, connection_count in group.connection_count_by_external_node_ids.items():
            if connection_count <= 0:
                removed_connected_node_ids.append(external_node_id)

        for removed_connected_node_id in removed_connected_node_ids:
            group.connection_count_by_external_node_ids.pop(removed_connected_node_id)

    def get_external_channel_ids_for_group(group):
        external_channel_ids = set()

        for channel_id, endpoint_count in group.endpoint_count_by_channel_id.items():
            if endpoint_count_by_channel_id[channel_id] != endpoint_count:
                external_channel_ids.add(channel_id)

        return external_channel_ids

    def is_valid_group(group):
        return (
            len(group.node_ids) < max_nodes_per_group
            and len(get_external_channel_ids_for_group(group)) <= max_channels_total
        )

    while len(node_ids_claimed) < len(node_ids_all):
        group = Group(len(groups_by_id) + 1)

        starting_node = get_random_id_from_set(get_unclaimed_min_connection_nodes())
        claim_node_id_for_group(group, starting_node)

        candidate_nodes = set(group.connection_count_by_external_node_ids.keys()) - node_ids_claimed

        while len(node_ids_claimed) < len(node_ids_all) and len(candidate_nodes) > 0:
            curr_node_id = candidate_nodes.pop()

            claim_node_id_for_group(group, curr_node_id)

            if is_valid_group(group):
                candidate_nodes.update(connected_node_ids_by_node_id[curr_node_id] - node_ids_claimed)
            else:
                disclaim_node_id_for_group(group, curr_node_id)

        groups_by_id[group.id] = group
        
    groups = list(groups_by_id.values())
    
    # SAVE
    def save_groups(directory, saved_groups):
        base_file_name = f'max_nodes_{max_nodes_per_group}_max_channels_{max_channels_total}_{len(saved_groups)}_{int(time.time()*1000)}'
        
        with open(f'results/{directory}/nodes/{base_file_name}', 'w') as file:
            for group in saved_groups:
                file.write(','.join([str(node_id) for node_id in list(group.node_ids)]) + "\n")
        
        with open(f'results/{directory}/channels/{base_file_name}', 'w') as file:
            for group in saved_groups:
                file.write(','.join([str(node_id) for node_id in list(get_external_channel_ids_for_group(group))]) + "\n")
                
    save_groups('groups', groups)
    save_groups('merged_groups', groups)
                
    merged_groups = copy.deepcopy(groups)
    random.shuffle(merged_groups)

    is_first_try = True
    is_merging = True
    curr_group_index = 0

    while is_first_try:
        while curr_group_index < len(merged_groups):
            curr_group = merged_groups[curr_group_index]
            is_completed_merge = False

            group_indexs = list(range(curr_group_index + 1, len(merged_groups)))
            random.shuffle(group_indexs)

            for group_index in group_indexs:
                group_node_ids = list(merged_groups[group_index].node_ids)

                for node_id in group_node_ids:
                    add_node_id_to_group(curr_group, node_id)

                if is_valid_group(curr_group):
                    del merged_groups[group_index]
                    merged_groups[curr_group_index] = curr_group
                    save_groups('merged_groups', merged_groups)
                    is_completed_merge = True
                    break

                for node_id in group_node_ids:
                    remove_node_id_from_group(curr_group, node_id)

            if not is_completed_merge:
                curr_group_index += 1
        
        is_first_try = False