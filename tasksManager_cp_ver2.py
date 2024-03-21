import json
from pycsp3 import *
from math import ceil

machines_array = []
tasks_array = []
ressources_incompatibilities=[]
n_ressources=0
def read_input(input_file):
    file = open(input_file)
    file_data = json.load(file)
    global n_ressources
    n_ressources=file_data['nResources']
    for i in range (int(file_data['nMachines'])):
        machines_array.append(i)
    for task in file_data['tests']:
        if len(task['machines'])>0:
            tasks_array.append([int(task['duration']), task['machines'], task['resources']])
        else:
            tasks_array.append([int(task['duration']), machines_array, task['resources']])
    
def generate_incompatibilities_by_ressources():
    tmp = []
    for i in range(len(tasks_array)):
        for j in range(i+1, len(tasks_array)):
            if not tasks_compatible(tasks_array[i], tasks_array[j]):
                tmp.append(j)
        ressources_incompatibilities.append(tmp)
        tmp=[]

def tasks_compatible(task1, task2):
    for ressource in task1[2]:
        if ressource in task2[2]:
            return False
    return True

def machineAcceptable(task, machine):
    return machine in tasks_array[task][1]

def get_worst_time():
    ressources_min_times=[]
    machine_times_any=[]
    machines_min_times=[]
    for i in range(len(machines_array)):
        machines_min_times.append(0)
    for i in range(n_ressources):
        ressources_min_times.append(0)
    for task in tasks_array:
        for ressource in task[2]:
            ressources_min_times[ressource]+=task[0]
        if task[1]==machines_array:
            machine_times_any.append(task[0])
        else:
            for machine in task[1]:
                machines_min_times[machine]+=task[0]
    machine_times_any= sorted(machine_times_any, reverse=True)
    for t in machine_times_any:
        machines_min_times.sort()
        machines_min_times[0]+=t # Supposing a task cannot be split between multiple machines
    #print(f' {ressources_min_times} - {machines_min_times} - {machines_min_times}')
    return max({max(ressources_min_times), max(machines_min_times)})
    
read_input('./t10-example.json')
generate_incompatibilities_by_ressources()
ntasks=len(tasks_array)
maxTime = get_worst_time() # redo !!
print(f'First estimation of tasks execution time : {maxTime}')

tasks_machines_vararrays = []
tasks_instants_vararrays = []
i=0
for task in tasks_array:
    tasks_machines_vararrays.append(VarArray(size=task[0], dom=range(len(machines_array)), id="task_"+str(i)+"_machines"))
    tasks_instants_vararrays.append(VarArray(size=task[0], dom=range(maxTime), id="task_"+str(i)+"_instant"))
    i+=1

satisfy(

    [task[i]+1==task[i+1] for task in tasks_instants_vararrays for i in range(len(task)-1)],
    
    [machineAcceptable(i,machine)
     for i in range(ntasks)
     for machine in tasks_machines_vararrays[i]],# tasks executed on valid machines
    
    [ instant != instant2
     for i in range(ntasks)
     for j in ressources_incompatibilities[i]
     for instant in tasks_instants_vararrays[i]
     for instant2 in tasks_instants_vararrays[j]],
    # no two incompatible tasks in same time

    [ If(tasks_instants_vararrays[i][instant_index_1] == tasks_instants_vararrays[j][instant_index_2],
        Then = tasks_machines_vararrays[i][instant_index_1]!=tasks_machines_vararrays[j][instant_index_2])
    for i in range(ntasks)
    for j in range(i+1, ntasks)
    for instant_index_1 in range(tasks_array[i][0])
    for instant_index_2 in range(tasks_array[j][0])],# no two tasks using same machine
)
minimize(
    Maximum(tasks_instants_vararrays[i][len(tasks_instants_vararrays[i])-1]
            for i in range(len(tasks_instants_vararrays)))
)
result = solve()
print(result)

if result in (SAT, OPTIMUM):
    machines_usages=[['  ' for _ in range(maxTime)] for _ in range(len(machines_array))]
    optimal_time=0
    for i in range(len(tasks_array)):
        optimal_time=max(optimal_time,values(tasks_instants_vararrays[i])[tasks_array[i][0]-1])
        c=str(i)
        for j in range(tasks_array[i][0]):
            machines_usages[values(tasks_machines_vararrays[i])[j]][values(tasks_instants_vararrays[i])[j]]= 't'+c
    print(f'Execution Time = {optimal_time+1}')
    for machine in machines_usages:
        print(machine)
    #print(range(maxTime))

