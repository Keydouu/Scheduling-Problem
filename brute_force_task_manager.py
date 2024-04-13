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
ressources_incompatibilities=[]
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
generate_incompatibilities_by_ressources()
tasks_machines = []
tasks_order= []
ends=VarArray(size=[ntasks], dom=range(2000))
for i in range(ntasks):
    tasks_order.append(Var(dom=range(ntasks), id='start_task'+str(i)))
    tasks_machines.append(Var(dom=set(tasks_array[i][1]), id='atask_machine'+str(i)))

satisfy(
    AllDifferent(tasks_order),
    [((tasks_order[i]!=0) | (end[i]==tasks_array[i][0]) )for i in range(ntasks)],
    [if((tasks_machines[i]==tasks_machines[j]) | (j in ressources_incompatibilities[i]),
        Then = () )
     for i in range(ntasks) for j in range(i+1, ntasks)]
)
minimize(
    Maximum(ends)
    #calculate_cost(tasks_order, tasks_machines)#, Sum(tasks_order)+Sum(tasks_machines))
)
result=solve(options=" -varh=Dom")
print(result)
def calculate_starts():
    ressources_free=[0 for i in range(n_ressources)]
    machines_free=[0 for i in range(len(machines_array))]
    free_indexs=[i for i in range(ntasks)]
    tasks_starts=[0 for _ in range(ntasks)]
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
                break
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