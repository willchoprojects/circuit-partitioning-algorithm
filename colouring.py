import os
import networkx as nx

dir_path = 'results/merged_groups/channels'

def main(digits):
    file_names = os.listdir(dir_path)

    for file_name in file_names:
        if file_name == "channels":
            continue

        parts = file_name.split("_")
        max_channels_index = parts.index("channels")
        max_channels = int(parts[max_channels_index+1])
        last_digit = int(file_name[-1])

        if last_digit not in digits:
            continue

        external_channel_id_sets = []
        with open(f'{dir_path}/{file_name}', 'r') as f:
            for line in f:
                row = line.strip().split(',')
                row_set = set(map(int, row))
                external_channel_id_sets.append(row_set)

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

        edge_pairs = []

        for external_channel_ids in external_channel_id_sets:
            curr_external_channel_ids = list(external_channel_ids)

            for i in range(len(curr_external_channel_ids)):
                for j in range(i + 1, len(curr_external_channel_ids)):
                    edge_pairs.append((curr_external_channel_ids[i], curr_external_channel_ids[j]))

        G = nx.Graph()
        G.add_edges_from(edge_pairs)

        is_trying = True
        is_min = False
        min_max_channels = max_channels

        while is_trying:
            try:
                colours = graph_coloring(G, min_max_channels)
                is_trying = False
            except Exception:
                is_min = True
                min_max_channels += 1

        strict_min_max_channels = min_max_channels

        if not is_min:
            for curr_max_channels in range(min_max_channels, 0, -1):
                try:
                    colours = graph_coloring(G, curr_max_channels)
                    strict_min_max_channels = curr_max_channels
                except Exception:
                    break

        new_file_name = file_name

        if strict_min_max_channels != max_channels:
            new_file_name += f'_actual_channels_{strict_min_max_channels}'

        with open(f'results/assigned_groups/{new_file_name}', 'w') as file:
            file.write(str(colours))
