class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.connections = []

    def __str__(self):
        return f'Node: id - {self.id}, connections - {[connection.get_simple_string() for connection in self.connections]}'
