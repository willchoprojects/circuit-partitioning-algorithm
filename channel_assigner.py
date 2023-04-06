import networkx as nx
import time

def graph_coloring(graph, m):
    colours = {}
    nodes = list(graph.nodes())

    nodes = sorted(nodes, key=lambda x: len(list(graph.neighbors(x))), reverse=True)

    for node in nodes:
        used_colours = set(colours.get(n, None) for n in graph.neighbors(node))
        available_colours = set(range(1, m+1)) - used_colours
        if available_colours:
            colours[node] = min(available_colours)
        else:
            raise Exception("Graph cannot be colored with %d colors" % m)

    return colours

def get_channel_assignment(edge_pairs, max_num_total_channels, desired_min_max_channels):
    G = nx.Graph()
    G.add_edges_from(edge_pairs)

    is_trying = True
    is_min = False
    min_max_channels = max_num_total_channels

    while is_trying:
        try:
            channel_assignment = graph_coloring(G, min_max_channels)
            is_trying = False
        except Exception:
            is_min = True
            min_max_channels += 1

    if not is_min:
        for curr_max_channels in range(min(min_max_channels, desired_min_max_channels), 0, -1):
            try:
                channel_assignment = graph_coloring(G, curr_max_channels)
            except Exception:
                break

    return channel_assignment

