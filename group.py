from collections import defaultdict

class Group:
    def __init__(self, group_id):
        self.id = group_id
        self.node_ids = set()
        self.connection_count_by_external_node_ids = defaultdict(int)
        self.endpoint_count_by_channel_id = defaultdict(int)

    def __str__(self):
        return f'Group: id - {self.id}, node_ids - {self.node_ids}'