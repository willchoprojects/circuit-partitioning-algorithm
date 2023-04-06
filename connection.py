class Connection:
    def __init__(self, connection_id, sender_node_id, receiver_node_id):
        self.id = connection_id
        self.sender_node_id = sender_node_id
        self.receiver_node_id = receiver_node_id
        self.channel_id = self.sender_node_id

    def get_simple_string(self):
        return f'({self.sender_node_id}-{self.receiver_node_id})'

    def __str__(self):
        return f'Connection: id - {self.id}, sender_node_id-receiver_node_id - {self.get_simple_string()}'