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
    ressources_limit=max(ressources_min_times)
    machines_limit=max(machines_min_times)
    print(f'R{ressources_limit} - M{machines_limit} ')
    return ressources_limit, machines_limit, max({ressources_limit, machines_limit})

generate_incompatibilities_by_ressources()
ntasks=len(tasks_array)
ressources_limit, machines_limit, maxTime = get_worst_time()
tasks_machines = []
tasks_order= []
tasks_starts= []
tasks_ends=[]
for i in range(ntasks):
    tasks_order.append(Var(dom=range(ntasks), id='start_task'+str(i)))
    tasks_machines.append(Var(dom=set(tasks_array[i][1]), id='task_machine'+str(i)))
    tasks_starts.append(Var(dom=range(maxTime-tasks_array[i][0]+1), id='start_task'+str(i)))
    tasks_ends.append(Var(dom=range(maxTime+1), id='end_task'+str(i)))

satisfy(
    AllDifferent(tasks_order),
    [(If(tasks_order[i]!=0, Then = tasks_starts[i]==0) )for i in range(ntasks)], #task 1 start at 0

    [(If(tasks_order[i]==tasks_order[j]+1,
         Then = (tasks_starts[j]>=tasks_starts[i])| (task) ) )
         for i in range(ntasks) for j in range(i, ntasks)],# respect the starting order
    #[ ((True))
    # for i in range(ntasks)
    # for j in ressources_incompatibilities[i]],


    [ If(tasks_order[i]==j,
         Then = tasks_ends[j]==max(tasks_array[i][0]+tasks_starts[j])
         for i in range(ntasks) for j in range(ntasks)]
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