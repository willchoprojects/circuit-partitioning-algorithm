import os
import partition_and_colour

num_repeats = 1000000

node_range = list(range(1, 135))
channel_range = list(range(3, 135))

base_directory = 'results'
nodes_directory = 'nodes'
channels_directory = 'channels'
channel_assignments_directory = 'channel_assignments'

directories = [
    base_directory,
    f'{base_directory}/{nodes_directory}',
    f'{base_directory}/{channels_directory}',
    f'{base_directory}/{channel_assignments_directory}',
]

def main():
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    for i in range(num_repeats):
        for num_nodes in node_range:
            for num_channels in channel_range:
                partition_and_colour.main(num_nodes, num_channels)