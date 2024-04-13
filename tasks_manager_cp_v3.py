import json
from pycsp3 import *

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
    ressources_limit=max(ressources_min_times)
    machines_limit=max(machines_min_times)
    print(f'R{ressources_limit} - M{machines_limit} ')
    return ressources_limit, machines_limit, max({ressources_limit, machines_limit})

test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[0])
generate_incompatibilities_by_ressources()
ntasks=len(tasks_array)
ressources_limit, machines_limit, maxTime = get_worst_time()
print(f'First estimation of tasks execution time : {maxTime}')

tasks_machines = []
tasks_starts= []
tasks_ends=[]

for i in range(ntasks):
    tasks_starts.append(Var(dom=range(ntasks+1), id='start_task'+str(i)))
    tasks_ends.append(Var(dom=range(tasks_array[i][0]-1,maxTime+1), id='end_task'+str(i)))
    tasks_machines.append(Var(dom=set(tasks_array[i][1]), id='task_machine'+str(i)))
tasks_ends.append(Var(dom={0}, id='myNull'))
def getEnd(index):
    if tasks_starts[index]<ntasks:
        return getEnd(tasks_starts[index])
    return duration(tasks_starts[index])
def duration(i):
    return tasks_array[i][0]
#tasks_starts = VarArray(size=[ntasks], dom=range(maxTime))
#Force a task To start at 0, after another task is done, or when ressource is free
satisfy(

    #tasks_starts[0]>=tasks_starts[1],#a poor man's attempt to break symmetry

    [tasks_starts[i]+duration(i)-1==tasks_ends[i] for i in range(ntasks)],
    
    [ ((tasks_ends[i] < tasks_ends[j]-tasks_array[j][0])
                | (tasks_ends[i]-tasks_array[i][0]> tasks_ends[j]))
     for i in range(ntasks)
     for j in ressources_incompatibilities[i]],
    # no two incompatible tasks in same time

    [ If(tasks_machines[i]==tasks_machines[j],
        Then = (tasks_starts[i] != tasks_starts[j]) )
    for i in range(ntasks)
    for j in range(i+1, ntasks)],# no two tasks using same machine

    [If(tasks_starts[i]==j, Then=tasks_ends[i]==tasks_ends[j]+tasks_array[i][0]-1) for i in range(ntasks) for j in range(ntasks+1)],#define tasks ends

    [ Sum((tasks_starts[i]==tasks_ends[j]) for j in range(ntasks+1))>0
       for i in range(ntasks)],# a task either start at t=0, or tight after the end of another task
    #[ If()]#
    
)
#minimize(
#    Maximum(
#        tasks_ends
#    )
#)
#how to break symetrie :
# 1) assure one task is before another ( more than one pair may fuck up everything )
# 2) force one machine to finish before another ?

result = solve(options="-t=60s")
print(result)


if result in (SAT, OPTIMUM):
    print(f'R{ressources_limit} - M{machines_limit} ')
    optimal_time=0
    for i in range(len(tasks_array)):
        optimal_time=max(optimal_time,value(tasks_starts[i])+tasks_array[i][0]-1)
    print(f'Execution Time = {optimal_time}')
    machines_usages=[{} for _ in range(len(machines_array))]
    for i in range(len(tasks_array)):
        start=values(tasks_starts)[i]
        str_start=str(start)
        m_indx = value(tasks_machines[i])
        machines_usages[m_indx]['s'+str_start+' t'+str(i)+' d'+str(tasks_array[i][0])+ ' e'+str(start+tasks_array[i][0]-1)]=start
    for machine in machines_usages:
        #machine.sort()
        print([key for key, value in sorted(machine.items(), key=lambda item: item[1])])
