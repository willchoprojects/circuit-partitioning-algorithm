import os
import colouring

digits_dict = {
    1: [0, 5],
    2: [1, 6],
    3: [2, 7],
    4: [3, 8],
    5: [4, 9]
}


base_directory = 'results'
assigned_groups_directory = 'assigned_groups'

directories = [
    base_directory,
    f'{base_directory}/{assigned_groups_directory}',
]

def main(index):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    colouring.main(digits_dict[index])
    