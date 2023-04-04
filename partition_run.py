import os
import partition

num_repeats = 1000000

node_range = list(range(1, 135))
channel_range = list(range(3, 135))

base_directory = 'results'
groups_directory = 'groups'
merged_groups_directory = 'merged_groups'
nodes_directory = 'nodes'
channels_directory = 'channels'

directories = [
    base_directory,
    f'{base_directory}/{groups_directory}',
    f'{base_directory}/{groups_directory}/{nodes_directory}',
    f'{base_directory}/{groups_directory}/{channels_directory}',
    f'{base_directory}/{merged_groups_directory}',
    f'{base_directory}/{merged_groups_directory}/{nodes_directory}',
    f'{base_directory}/{merged_groups_directory}/{channels_directory}',
]

def main():
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    for i in range(num_repeats):
        for num_nodes in node_range:
            for num_channels in channel_range:
                partition.main(num_nodes, num_channels)