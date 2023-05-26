from graph import Graph
from logger import Logger
from table_maker import table_str
from tasks import *
from config import datasets
import os
import json

properties_path = '../properties/properties.json'

tasks_to_output = [{'name' : 'Number of vertices, number of edges, density...', 'func' : task_1}, 
                   {'name' : 'Radius, network diameter, 90 percentile...', 'func' : task_2}, 
                   {'name' : 'Average cluster coefficient', 'func' : task_3}, 
                   {'name' : 'The coefficient of assortativity', 'func' : task_4}, 
                   {'name' : 'Prediction model', 'func' : None}]

if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

def __incorrect_input(range_to : int, output : str):
    output = f'Input must be a number of range [-1, {range_to}]\n\n'
    output += 'Press any button to continue'
    clear()
    print(output)
    input()
    output = ''

def __results_as_table(graph : Graph, function : callable, properties : dict, table_len : int = 100) -> str:
    heading, values = function(graph, properties)
    if (heading is None) or (values is None):
        return ''
    return table_str(heading, values, table_len)

def __get_properties(dataset : dict) -> dict:
    try:
        if not (os.path.isfile(properties_path)):
            return dict()
        with open(properties_path, 'r') as file:
            all_props = json.load(file)
        return all_props[dataset['file_name']] if (dataset['file_name'] in all_props) else dict()
    except OSError:
        print("Could not open/read file: ", properties_path)
        input()
    except Exception:
        print("Could not parse json: ", properties_path)
        input()

    pass

def __save_properties(dataset : dict, properties : dict) -> None:
    try:
        if (os.path.isfile(properties_path)):
            with open(properties_path, 'r') as file:
                all_props = json.load(file)
        else:
            all_props =  dict()

        all_props[dataset['file_name']] = properties

        with open(properties_path, 'w+') as file:
            json.dump(all_props, file)
    except OSError:
        print("Could not open/read file: ", properties_path)
        input()
    except Exception:
        print("Could not parse json: ", properties_path)
        input()

def __results_section(dataset_idx : int, output : str = '', graph : Graph = None) -> str:
    current_dataset = datasets[dataset_idx]
    file_path = '../data/' + current_dataset['file_name']
    timestamp_col = current_dataset['timestamp_col']
    weight_col = current_dataset['weight_col']
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
    properties = __get_properties(current_dataset)

    if (len(properties) < 9) and (graph is None):
        if (os.path.isfile(file_path)):
            graph = Graph(file_path, timestamp_col, weight_col, number_of_lines_to_skip)
        else:
            clear()
            print('Files for graph initialization were not found\n')
            print('Press any button to continue')
            input()
            return None, __datasets_section, None

    while True:
        output += 'You have chosen: ' + str(current_dataset['file_name']) + '\n\n'
        output += 'Select a task to output:\n\n'
        for task_idx in range(len(tasks_to_output)):
            output += ' ' + str(task_idx) + ' : ' + str(tasks_to_output[task_idx]['name']) + '\n'
        output += '\n-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        task_idx = input()

        if (task_idx == '-1'):
            return None, __datasets_section, None

        if not (task_idx.isdigit()):
            __incorrect_input(len(tasks_to_output) - 1, output)
            output = ''
            continue
        
        task_idx = int(task_idx)
        if (task_idx == len(tasks_to_output) - 1):
            return dataset_idx, __prediction_section, graph


        if (task_idx < 0) or (task_idx >= len(tasks_to_output)):
            __incorrect_input(len(tasks_to_output) - 1, output)
            output = ''
            continue

        clear()
        print('Wait a moment...')
        table = __results_as_table(graph, tasks_to_output[task_idx]['func'], properties, table_len=100) + '\n\n'
        if not (graph is None):
            __save_properties(current_dataset, properties)
        output = 'You have chosen: ' + str(tasks_to_output[task_idx]['name']) + '\n\n' + table
        output += 'Press any button to continue'
        clear()
        print(output)
        input()
        output = ''


def __prediction_section(dataset_idx : int, output : str = '', graph : Graph = None) -> tuple:
    while True:
        output += 'Select a type of prediction model:\n\n'
        output += ' 0 : Static\n'
        output += ' 1 : Temporal\n\n'
        output += '-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        task_idx = input()

        if (task_idx == '-1'):
            return dataset_idx, __results_section, graph

        if not (task_idx.isdigit()):
            __incorrect_input(1, output)
            output = ''
            continue
        
        task_idx = int(task_idx)
        if (task_idx == 0) or (task_idx == 1):
            clear()
            print('Close the window to continue')
            ans = task_5(datasets[dataset_idx], static=(task_idx == 0))
            if (ans is None):
                output = 'No data has been collected for this graph\n\n'
                output += 'Press any button to continue'
                clear()
                print(output)
                input()
                return dataset_idx, __results_section, graph
            else:
                output = 'You have chosen: ' + str(datasets[dataset_idx]['file_name'])
                output +=(' (static model)' if (task_idx == 0) else ' (temporal model)') + '\n\n'
                output += table_str(ans[0], ans[1], 100) + '\n\n'
                output += 'Press any button to continue'
                clear()
                print(output)
                input()
            output = ''
        else:
            __incorrect_input(1, output)
            output = ''


def __datasets_section(dataset_idx : int, output : str = '', graph : Graph = None) -> tuple:
    while True:
        output += 'Select a dataset:\n\n'
        for idx in range(len(datasets)):
            output += ' ' + str(idx) + ' : ' + datasets[idx]['file_name'] + '\n'
        output += '\n-1 : Exit\n'
        output += '\nEnter the number: '

        clear()
        print(output, end='')
        idx = input()

        if (idx == '-1'):
            return int(idx), None, None

        if not (idx.isdigit()):
            __incorrect_input(len(datasets) - 1, output)
            output = ''
            continue
        
        idx = int(idx)
        if (idx < 0) or (idx >= len(datasets)):
            __incorrect_input(len(datasets) - 1, output)
            output = ''
            continue
        
        clear()
        print('Wait a moment...')
        return idx, __results_section, None


def launch() -> None:
    console_state = __datasets_section
    graph = None
    dataset_idx = 0

    while (True):
        dataset_idx, console_state, graph = console_state(dataset_idx=dataset_idx, graph=graph) 
        if (console_state is None):
            return
