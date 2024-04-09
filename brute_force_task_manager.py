import json
from pycsp3 import *

machines_array = []
tasks_array = []
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
    
read_input('./t10-example.json')
#read_input('./t20m10r3-1.json')
#read_input('./t40m10r3-2.json')
ntasks=len(tasks_array)
def calculate_cost(order, machines):
    ressources_free=[0 for i in range(n_ressources)]
    machines_free=[0 for i in range(len(machines_array))]
    free_indexs=[i for i in range(ntasks)]
    cost=0
    for pos in range(ntasks):#parcour order
        for task in free_indexs:
            if order[task]==pos:
                m=machines[task].value
                start_time=machines_free[m]
                for ressource in tasks_array[task][2]:
                    start_time=max(start_time, ressources_free[ressource])
                for ressource in tasks_array[task][2]:
                    ressources_free[ressource]=start_time+tasks_array[task][0]
                cost+=start_time-machines_free[m]
                machines_free[m]=start_time+tasks_array[task][0]
                free_indexs.remove(task)
                break;
    score=max(machines_free)
    for machine in machines_free:
        cost+=score-machine
    return cost
tasks_machines = []
tasks_order= []
for i in range(ntasks):
    tasks_order.append(Var(dom=range(ntasks), id='start_task'+str(i)))
    tasks_machines.append(Var(dom=set(tasks_array[i][1]), id='task_machine'+str(i)))
satisfy(
    AllDifferent(tasks_order)
)
#minimize(
#    calculate_cost(tasks_order, tasks_machines)
#)
result=solve()
print(result)
def calculate_starts():
    ressources_free=[0 for i in range(n_ressources)]
    machines_free=[0 for i in range(len(machines_array))]
    free_indexs=[i for i in range(ntasks)]
    tasks_starts=[0 for i in range(ntasks)]
    for pos in range(ntasks):#parcour order
        for task in free_indexs:
            if values(tasks_order)[task]==pos:
                print(tasks_machines[task])
                print(value(tasks_machines[task]))
                m=value(tasks_machines[task])
                start_time=machines_free[m]
                for ressource in tasks_array[task][2]:
                    start_time=max(start_time, ressources_free[ressource])
                for ressource in tasks_array[task][2]:
                    ressources_free[ressource]=start_time+tasks_array[task][0]
                machines_free[m]=start_time+tasks_array[task][0]
                tasks_starts[task]=start_time
                free_indexs.remove(task)
                break;
    return tasks_starts

if result in (SAT, OPTIMUM):
    optimal_time=0
    tasks_starts=calculate_starts()
    for i in range(len(tasks_array)):
        optimal_time=max(optimal_time,tasks_starts[i]+tasks_array[i][0])
    print(f'Execution Time = {optimal_time}')
    machines_usages=[{} for _ in range(len(machines_array))]
    for i in range(len(tasks_array)):
        start=tasks_starts[i]
        str_start=str(start)
        machines_usages[values(tasks_machines)[i]]['s'+str_start+' t'+str(i)+' d'+str(tasks_array[i][0])+ ' e'+str(start+tasks_array[i][0]-1)]=start
    for machine in machines_usages:
        #machine.sort()
        print([key for key, value in sorted(machine.items(), key=lambda item: item[1])])
#order only
# machines uses
# calculate cost