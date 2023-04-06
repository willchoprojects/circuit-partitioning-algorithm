import os
import time
from collections import defaultdict

def compile_data(compiled_data_directory, results_directories, is_expanding=False, max_num_gates_per_cell=None, max_num_total_channels=None):
    if not os.path.exists(compiled_data_directory):
        os.makedirs(compiled_data_directory)

    file_suffix = ''
    if is_expanding:
        file_suffix = '_expanded'

    data = defaultdict(lambda: float('inf'))

    for base_directory in results_directories:
        for file_name in os.listdir(f'{base_directory}nodes'):
            parts = file_name.split('_')

            max_nodes_index = parts.index('nodes') + 1
            max_channels_index = parts.index('channels') + 1
            num_cells_index = float('inf')
            try:
                num_cells_index = parts.index('cells') + 1
            except Exception:
                num_cells_index = parts.index('channels') + 2

            max_nodes = int(parts[max_nodes_index])
            max_channels = int(parts[max_channels_index])
            num_cells = int(parts[num_cells_index])

            data[(max_nodes,max_channels)] = min(data[(max_nodes,max_channels)], num_cells)

    if is_expanding:
        for i in range(1, max_num_gates_per_cell + 1):
            prev_min = float('inf')
            for j in range(1, max_num_total_channels):
                prev_min = min(prev_min, data[i, j])
                data[i, j] = prev_min

        for i in range(1, max_num_total_channels + 1):
            prev_min = float('inf')
            for j in range(1, max_num_gates_per_cell):
                prev_min = min(prev_min, data[j, i])
                data[j, i] = prev_min

    with open(f'{compiled_data_directory}num_cells_data{file_suffix}_{int(time.time())}.csv', 'w') as file:
        for i in range(1, 140):
            row_strings = []
            for j in range(1, 140):
                row_strings.append(str(data[i, j]))

            file.write(','.join(row_strings) + '\n')

