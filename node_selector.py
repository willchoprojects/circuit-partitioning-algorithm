import random

class NodeSelector():
    def __init__(self, node_ids_all, node_id_by_connection_count, is_minimizing=True, is_leaky_formation=False, leaky_formation_threshold=0.8):
        self.node_ids_all = node_ids_all
        self.node_id_by_connection_count = node_id_by_connection_count
        self.leaky_formation_threshold = leaky_formation_threshold

        if is_minimizing:
            if is_leaky_formation:
                self.get_next_nodes = self.get_minimal_connection_node_ids_leaky
            else:
                self.get_next_nodes = self.get_minimal_connection_node_ids
        else:
            self.get_next_nodes = self.get_all_unclaimed_node_ids

    def get_minimal_connection_node_ids_leaky(self, node_ids_claimed):
        for i in range (1, max(self.node_id_by_connection_count.keys()) + 1):
            curr_node_ids = self.node_id_by_connection_count[i] - node_ids_claimed
            if len(curr_node_ids) > 0 and random.random() <= self.leaky_formation_threshold:
                return curr_node_ids

        return curr_node_ids

    def get_minimal_connection_node_ids(self, node_ids_claimed):
        for i in range (1, max(self.node_id_by_connection_count.keys()) + 1):
            curr_node_ids = self.node_id_by_connection_count[i] - node_ids_claimed
            if len(curr_node_ids) > 0:
                return curr_node_ids

        return curr_node_ids

    def get_all_unclaimed_node_ids(self, node_ids_claimed):
        return self.node_ids_all - node_ids_claimed
