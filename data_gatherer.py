import os
from collections import defaultdict

data = defaultdict(lambda: float('inf'))

for file_name in os.listdir('results/assigned_groups'):
    parts = file_name.split('_')
    max_nodes = int(parts[2])
    if 'actual' in parts:
        max_channels_index = parts.index('actual') + 2
    else:
        max_channels_index = parts.index('channels') + 1
    max_channels = int(parts[max_channels_index])

    num_cells = int(parts[6])
    
    data[(max_nodes,max_channels)] = min(data[(max_nodes,max_channels)], num_cells)

with open(f'data.csv', 'w') as file:
    for pair, cells in data.items():
        file.write(f'{pair[0]},{pair[1]},{cells}' + '\n')