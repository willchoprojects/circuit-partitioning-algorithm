from collections import defaultdict

def get_connection_count_by_node_id(connections_by_id):
    connection_count_by_node_id = defaultdict(int)

    for connection in connections_by_id.values():
        connection_count_by_node_id[connection.sender_node_id] += 1
        connection_count_by_node_id[connection.receiver_node_id] += 1

    return dict(connection_count_by_node_id)

def get_node_id_by_connection_count(connection_count_by_node_id):
    node_id_by_connection_count = defaultdict(set)

    for node_id, connection_count in connection_count_by_node_id.items():
        node_id_by_connection_count[connection_count].add(node_id)

    return dict(node_id_by_connection_count)

def get_connected_node_ids_by_node_id(connections_by_id):
    connected_node_ids_by_node_id = defaultdict(set)

    for connection in connections_by_id.values():
        connected_node_ids_by_node_id[connection.sender_node_id].add(connection.receiver_node_id)
        connected_node_ids_by_node_id[connection.receiver_node_id].add(connection.sender_node_id)

    return dict(connected_node_ids_by_node_id)

def get_endpoint_count_by_channel_id(connections_by_id):
    endpoint_count_by_channel_id = defaultdict(int)

    for connection in connections_by_id.values():
        endpoint_count_by_channel_id[connection.channel_id] += 2

    return dict(endpoint_count_by_channel_id)

def get_channel_id_count_by_node_id(connections_by_id):
    channel_id_count_by_node_id = defaultdict(lambda: defaultdict(int))

    for connection in connections_by_id.values():
        channel_id_count_by_node_id[connection.sender_node_id][connection.channel_id] += 1
        channel_id_count_by_node_id[connection.receiver_node_id][connection.channel_id] += 1

    return dict(channel_id_count_by_node_id)