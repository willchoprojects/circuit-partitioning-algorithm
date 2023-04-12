import os
import circuit_data_manager
from circuit_partitioner import CircuitPartitioner
from group import Group

def get_input_name_for(node_id):
    if type(node_id) == int:
        return f'in{node_id}'
    return f'{node_id[0]}{node_id[-1]}'

def get_output_name_for(node_id):
    if type(node_id) == int:
        return f'out{node_id}'
    return f'{node_id[0]}{node_id[-1]}'

def get_gate_name_for(node_id):
    if type(node_id) == int:
        return f'g{node_id}'
    return f'{node_id[0]}{node_id[-1]}'

def generate(circuit_file_path, results_base_directory, result_file_name, output_file_path):
    partitioner = CircuitPartitioner(circuit_file_path, '', 8, 4)
    nodes_by_group_id = circuit_data_manager.load_circuit_groups(results_base_directory, result_file_name, partitioner.nodes_by_id)

    groups_by_id = {}

    for group_id, nodes in nodes_by_group_id.items():
        group = Group(group_id)

        for node in nodes:
            partitioner.add_node_id_to_group(group, node.id)

        groups_by_id[group.id] = group
        
    nodes_by_id, connections_by_id = circuit_data_manager.load_circuit(circuit_file_path, True)
    
    group_input_node_ids_by_group_id = {}
    group_output_node_ids_by_group_id = {}

    for group in groups_by_id.values():
        group_input_node_ids = set()
        group_output_node_ids = set()

        for connection in connections_by_id.values():
            if connection.sender_node_id in group.node_ids:
                group_output_node_ids.add(connection.receiver_node_id)

            if connection.receiver_node_id in group.node_ids:
                group_input_node_ids.add(connection.sender_node_id)

        group_input_node_ids_by_group_id[group.id] = group_input_node_ids - group.node_ids
        group_output_node_ids_by_group_id[group.id] = group_output_node_ids - group.node_ids

    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    for group_id, group in groups_by_id.items():
        input_names = [get_input_name_for(node_id) for node_id in group_input_node_ids_by_group_id[group_id]]
        output_names = [get_output_name_for(node_id) for node_id in group_output_node_ids_by_group_id[group_id]]
        gate_names = [get_gate_name_for(node_id) for node_id in group.node_ids]

        with open(f'{output_file_path}group_{group_id}.v', 'w') as f:
            f.write(f'module Main({", ".join(input_names + output_names)});\n')
            f.write(f'\toutput {", ".join(output_names)};\n')
            f.write(f'\tinput {", ".join(input_names)};\n')
            f.write(f'\twire {", ".join(gate_names)};\n')
            f.write(f'\n')

            for gate_name in gate_names:
                input_node_ids = nodes_by_id[int(gate_name[1:])].get_input_node_ids()

                if len(input_node_ids) == 2:
                    f.write(f'\tassign {gate_name} = {input_node_ids.pop()} ~| {input_node_ids.pop()};\n')
                if len(input_node_ids) == 1:        
                    f.write(f'\tassign {gate_name} = ~{input_node_ids.pop()};\n')

            f.write(f'\n')
            f.write(f'endmodule')