import json
from pycsp3 import *

machines_array = []
tasks_numbers = []
tasks_array = []
worst_time_possible=0
realTasks=0
def read_input(input_file):
    file = open(input_file)
    file_data = json.load(file)
    i=0
    for i in range (int(file_data['nMachines'])):
        machines_array.append(i)
    for task in file_data['tests']:
        if len(task['machines'])>0:
            tasks_array.append([task['duration'], task['machines'], task['resources']])
        else:
            tasks_array.append([task['duration'], machines_array, task['resources']])
        tasks_numbers.append(i)
        i+=1
    
def getRessources(task_number):
    if task_number in tasks_numbers:
        return tasks_array[task_number][2] 
    return []

test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[0])
worst_time_possible=15#optimize later
tasks_ends = VarArray(size=[len(tasks_numbers)])
print(worst_time_possible)
print(len(machines_array))
time_table = VarArray(size=[15,3], dom=range(len(tasks_numbers)+3))

# tasks_ends = [ 1, 5, 4]
# time_table = array of instints => instant = array or machines' action => machine action = [task_number, array_ressource]
satisfy(
    [(Sum((active_task==current_task) for active_task in time_table)==tasks_array[current_task][0])
     for current_task in tasks_numbers], # each task is done exactly it duration time

    [[AllDifferent(time_table[i])]for i in worst_time_possible],# each task is done once at an instant

    [[([not (ressource in getRessources(nextMachine)) ] for nextMachine in range (machine_n, len(machines_array)))for ressource in getRessources(time_table[instant_n][machine_n])]
     for machine_n in len(machines_array) for instant_n in worst_time_possible],#each ressource is used once at an instant

    [If(time_table[instant_n][machine_n] < len(tasks_numbers), Then = machine_n in tasks_array[time_table[instant_n][machine_n]][1])
     for machine_n in len(machines_array) for instant_n in worst_time_possible]#each task is in a valid machine
)
print(solve())
minimize([
    max(tasks_ends)]
)