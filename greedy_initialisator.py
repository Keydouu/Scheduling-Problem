#greedy initialisator
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
    
def generate_incompatibilities_by_ressources(order):
    tmp = []
    for i in range(len(tasks_array)):
        for j in range(len(tasks_array)):
            if i!=j:
                if not tasks_compatible(tasks_array[i], tasks_array[j]):
                    tmp.append(j)
        ressources_incompatibilities.append(tmp)
        tmp=[]

def tasks_compatible(task1, task2):
    for ressource in task1[2]:
        if ressource in task2[2]:
            return False
    return True
def get_lower_bound():
    ressources_min_times=[0 for _ in range(n_ressources)]
    for task in tasks_array:
        for ressource in task[2]:
            ressources_min_times[ressource]+=task[0]
    return max(ressources_min_times)-1

test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[2])
ntasks=len(tasks_array)
greedyOrder = sorted(range(ntasks), key=lambda i: (-tasks_array[i][0], len(tasks_array[i][1])))
print(f'init : {greedyOrder}')
generate_incompatibilities_by_ressources(greedyOrder)
ntasks=len(tasks_array)
#output = ""
#for i in range(ntasks):
#    if len(ressources_incompatibilities[i])>0:
#        output+='t'+str(i)+' - '+str(ressources_incompatibilities[i])+'|'
#print(f'{output}')
tasks_machines = []
tasks_starts= []
worst=1
for i in range(ntasks):
    j=greedyOrder[i]
    tasks_machines.append(Var(dom=set(tasks_array[j][1]), id='task_machine'+str(j)))
    tasks_starts.append(Var(dom=range(0,worst), id='start_task'+str(j)))
    worst+=tasks_array[j][0]
lower_bound=get_lower_bound()
print(f"upper bound = {worst}")
print(f"lower bound = {lower_bound}")
score = Var(dom=range(lower_bound+1, worst))
satisfy(
    #tasks_starts[greedyOrder[0]]==0,#first task start at 0

    [tasks_starts[i+1]>=tasks_starts[i] for i in range(ntasks-1)],
    [tasks_starts[i+1]<=tasks_starts[i]+tasks_array[greedyOrder[i]][0] for i in range(ntasks-1)],
    #respecting the order

    [ If(tasks_starts[i]!=tasks_starts[i+1],
        Then=Sum(
            (tasks_starts[i+1]==tasks_starts[j]+tasks_array[greedyOrder[j]][0])
            for j in range(i+1))>=1)
       for i in range(ntasks-1)],# a task start right after the end of another task ( or 0 )
    
    [  (tasks_starts[greedyOrder.index(j)]+tasks_array[j][0] <= tasks_starts[i])|
     (tasks_starts[i]+tasks_array[greedyOrder[i]][0] <= tasks_starts[greedyOrder.index(j)])
        for i in range(ntasks)
        for j in ressources_incompatibilities[greedyOrder[i]]],
    # no two incompatible tasks in same time

    [ If(tasks_machines[i]==tasks_machines[j],
        Then = ((tasks_starts[i]+tasks_array[greedyOrder[i]][0] <= tasks_starts[j])
                | (tasks_starts[i]>= tasks_starts[j]+tasks_array[greedyOrder[j]][0])) )
    for i in range(ntasks)
    for j in range(i+1, ntasks)],# no two tasks using same machine
    score==Maximum((tasks_starts[i]+tasks_array[i][0])
                for i in range(ntasks))
)
minimize(
    score
)
#how to break symetrie :
# 1) assure one task is before another ( more than one pair may fuck up everything )
# 2) force one machine to finish before another ?
init_time=str(int(60*ntasks/len(machines_array)))
print(f"allocated initialisation time = {init_time}seconds")
result = solve(options="-t="+init_time+"s")
print(result)
if result in (SAT, OPTIMUM):
    maxend=0
    #optimal_time=0
    #for i in range(len(tasks_array)):
    #    optimal_time=max(optimal_time,values(tasks_starts)[i]+tasks_array[i][0])
    #print(f'Execution Time = {optimal_time} - {value(score)}')
    #print(f'Execution Time = {value(score)}')
    machines_usages=[{} for _ in range(len(machines_array))]
    for i in range(len(tasks_array)):
        start=values(tasks_starts)[i]
        str_start=str(start)
        j=greedyOrder[i]
        end=start+tasks_array[j][0]-1
        maxend=max(maxend,end)
        machines_usages[values(tasks_machines)[i]]['s'+str_start+' t'+str(j)+' d'+str(tasks_array[j][0])+ ' e'+str(end)]=start
    print(f"score = {maxend}")
    for i in range(len(machines_usages)):
        machine=machines_usages[i]
        print(f"M{i}\t{[key for key, value in sorted(machine.items(), key=lambda item: item[1])]}")
#order only
# machines uses
# calculate cost
    for filename in os.listdir("c:/Users/Youness/Desktop/CSP/tasksManager/"):
        if filename.endswith(".log"):
            os.remove("c:/Users/Youness/Desktop/CSP/tasksManager/"+filename)