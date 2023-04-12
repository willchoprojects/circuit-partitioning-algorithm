import random
import copy
import circuit_data_manager
import circuit_cacher
from node_selector import NodeSelector
from group import Group
import channel_assigner

class CircuitPartitioner():
    def __init__(self, circuit_file_path, results_base_directory, max_num_gates_per_cell, max_num_total_channels, is_saving_intermediates=False, max_total_channels_ceiling=float('inf'), max_num_groups=float('inf'), is_minimizing=True, is_leaky_validation=False, leaky_validation_threshold=0.9, is_leaky_formation=False, leaky_formation_threshold=0.8):
        self.results_base_directory = results_base_directory
        self.circuit_file_path = circuit_file_path
        self.is_saving_intermediates = is_saving_intermediates

        self.groups_by_id = {}
        self.nodes_by_id, self.connections_by_id = circuit_data_manager.load_circuit(self.circuit_file_path)
        self.node_ids_all = set(self.nodes_by_id.keys())

        self.connection_count_by_node_id = circuit_cacher.get_connection_count_by_node_id(self.connections_by_id)
        self.node_id_by_connection_count = circuit_cacher.get_node_id_by_connection_count(self.connection_count_by_node_id)
        self.connected_node_ids_by_node_id = circuit_cacher.get_connected_node_ids_by_node_id(self.connections_by_id)
        self.endpoint_count_by_channel_id = circuit_cacher.get_endpoint_count_by_channel_id(self.connections_by_id)
        self.channel_id_count_by_node_id = circuit_cacher.get_channel_id_count_by_node_id(self.connections_by_id)

        self.max_num_gates_per_cell = max_num_gates_per_cell
        self.max_num_total_channels = max_num_total_channels
        self.max_total_channels_ceiling = max_total_channels_ceiling
        self.max_num_groups = max_num_groups
        self.node_selector = NodeSelector(self.node_ids_all, self.node_id_by_connection_count, is_minimizing=is_minimizing, is_leaky_formation=is_leaky_formation, leaky_formation_threshold=leaky_formation_threshold)

        if is_leaky_validation:
            self.is_valid_group = self.is_valid_group_leaky
            self.validation_leaky_threshold = leaky_validation_threshold
        else:
            self.is_valid_group = self.is_valid_group_strict

    def claim_node_id_for_group(self, group, node_id):
        self.node_ids_claimed.add(node_id)
        self.add_node_id_to_group(group, node_id)

    def add_node_id_to_group(self, group, node_id):
        group.node_ids.add(node_id)

        for channel_id, count in self.channel_id_count_by_node_id[node_id].items():
            group.endpoint_count_by_channel_id[channel_id] += count

        for connected_node_id in self.connected_node_ids_by_node_id[node_id]:
            group.connection_count_by_external_node_ids[connected_node_id] += 1

    def disclaim_node_id_for_group(self, group, node_id):
        self.node_ids_claimed.remove(node_id)
        self.remove_node_id_from_group(group, node_id)

    def remove_node_id_from_group(self, group, node_id):
        group.node_ids.remove(node_id)

        for channel_id, count in self.channel_id_count_by_node_id[node_id].items():
            group.endpoint_count_by_channel_id[channel_id] -= count

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

    def is_valid_group_strict(self, group):
        return (
            len(group.node_ids) <= self.max_num_gates_per_cell
            and len(self.get_external_channel_ids_for_group(group)) <= self.max_num_total_channels
        )

    def is_valid_group_leaky(self, group):
        return random.random() > self.validation_leaky_threshold or (
            len(group.node_ids) <= self.max_num_gates_per_cell
            and len(self.get_external_channel_ids_for_group(group)) <= self.max_num_total_channels
        )

    def get_external_channel_ids_for_group(self, group):
        external_channel_ids = set()

        for channel_id, endpoint_count in group.endpoint_count_by_channel_id.items():
            if self.endpoint_count_by_channel_id[channel_id] != endpoint_count:
                external_channel_ids.add(channel_id)

        return external_channel_ids

    def get_groups(self):
        self.node_ids_claimed = set()

        while len(self.node_ids_claimed) < len(self.node_ids_all):
            group = Group(len(self.groups_by_id) + 1)

            starting_node = random.choice(tuple(self.node_selector.get_next_nodes(self.node_ids_claimed)))

            self.claim_node_id_for_group(group, starting_node)

            candidate_nodes = set(group.connection_count_by_external_node_ids.keys()) - self.node_ids_claimed

            while len(self.node_ids_claimed) < len(self.node_ids_all) and len(candidate_nodes) > 0:
                curr_node_id = candidate_nodes.pop()

                self.claim_node_id_for_group(group, curr_node_id)

                if self.is_valid_group(group):
                    candidate_nodes.update(self.connected_node_ids_by_node_id[curr_node_id] - self.node_ids_claimed)
                else:
                    self.disclaim_node_id_for_group(group, curr_node_id)

            self.groups_by_id[group.id] = group

        return list(self.groups_by_id.values())

    def get_edge_pairs(self, groups):
        edge_pairs = []
        for curr_merged_group in groups:
            curr_external_channel_ids = list(self.get_external_channel_ids_for_group(curr_merged_group))

            for i in range(len(curr_external_channel_ids)):
                for j in range(i + 1, len(curr_external_channel_ids)):
                    edge_pairs.append((curr_external_channel_ids[i], curr_external_channel_ids[j]))

        return edge_pairs

    def check_and_save_assignment(self, groups, is_saving=False):
        channel_assignment = channel_assigner.get_channel_assignment(self.get_edge_pairs(groups), self.max_num_total_channels, self.max_total_channels_ceiling)

        for group in groups:
            for channel_id, endpoint_count in group.endpoint_count_by_channel_id.items():
                endpoint_count_temp[channel_id] += endpoint_count

        if endpoint_count_temp != self.endpoint_count_by_channel_id:
            raise Exception("ASD")

        if is_saving and len(set(channel_assignment.values())) <= self.max_total_channels_ceiling and len(groups) <= self.max_num_groups:
            circuit_data_manager.save_circuit_groups(self.results_base_directory, groups, channel_assignment)

    def attempt_merges(self, groups):
        merged_groups = copy.deepcopy(groups)
        random.shuffle(merged_groups)

        curr_group_index = 0
        is_merging = True

        self.check_and_save_assignment(merged_groups, True)

        while is_merging and len(merged_groups) > 1:
            is_merging = False

            while curr_group_index < len(merged_groups):
                curr_group = merged_groups[curr_group_index]
                is_completed_merge = False

                group_indexs = list(range(curr_group_index + 1, len(merged_groups)))
                random.shuffle(group_indexs)

                for group_index in group_indexs:
                    group_node_ids = list(curr_group.node_ids) + list(merged_groups[group_index].node_ids)

                    curr_merged_group = Group(curr_group.id)

                    for node_id in group_node_ids:
                        self.add_node_id_to_group(curr_merged_group, node_id)

                    if self.is_valid_group(curr_merged_group):
                        del merged_groups[group_index]
                        merged_groups[curr_group_index] = curr_merged_group

                        self.check_and_save_assignment(merged_groups, self.is_saving_intermediates)

                        is_completed_merge = True
                        is_merging = True
                        break

                if not is_completed_merge:
                    curr_group_index += 1

        self.check_and_save_assignment(merged_groups, True)

    def generate_partitions(self):
        groups = self.get_groups()
        self.attempt_merges(groups)
