class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.connections = []
        
    def get_input_node_ids(self):
        input_node_ids = set()
        
        for connection in self.connections:
            if connection.receiver_node_id == self.id:
                input_node_ids.add(connection.sender_node_id)
        
        return input_node_ids

    def __str__(self):
        return f'Node: id - {self.id}, connections - {[connection.get_simple_string() for connection in self.connections]}'
