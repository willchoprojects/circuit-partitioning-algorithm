import os
from circuit_partitioner import CircuitPartitioner

nodes_directory = 'nodes/'
channels_directory = 'channels/'

def run(max_num_gates_per_cell_list, max_num_total_channels_list, circuit_file_path, is_saving_intermediates=False, results_base_directory='results/', num_repeats=1000000, desired_min_max_channels=float('inf'), max_num_groups=float('inf'), max_num_total_channels_ceiling=float('inf'), is_minimizing=True, is_leaky_validation=False, leaky_validation_threshold=0.9, is_leaky_formation=False, leaky_formation_threshold=0.8):
    directories = [
        results_base_directory,
        f'{results_base_directory}{nodes_directory}',
        f'{results_base_directory}{channels_directory}',
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    for i in range(num_repeats):
        for max_num_total_channels in max_num_total_channels_list:
            for max_num_gates_per_cell in max_num_gates_per_cell_list:
                partitioner = CircuitPartitioner(circuit_file_path, results_base_directory, max_num_gates_per_cell, max_num_total_channels, is_saving_intermediates, desired_min_max_channels, max_num_groups, max_num_total_channels_ceiling, is_minimizing, is_leaky_validation, leaky_validation_threshold, is_leaky_formation, leaky_formation_threshold)
                partitioner.generate_partitions()