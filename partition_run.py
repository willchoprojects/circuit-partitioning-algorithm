import partition

node_range = list(range(1, 131))
channel_range = list(range(3, 131))

def main():
    while True:
        for num_nodes in node_range:
            for num_channels in channel_range:
                partition.main(num_nodes, num_channels)