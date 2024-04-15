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
    
test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[1])
ressources_incompatibilities=[]
def generate_incompatibilities_by_ressources():
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
tasks_order= VarArray(size=ntasks, dom=range(ntasks))
tasks_starts= []
#tasks_ends=[]*
#priorityVars= ""
for i in range(ntasks):
    nbr=str(i)
    tasks_machines.append(Var(dom=set(tasks_array[i][1]), id='task_machine'+nbr))
    tasks_starts.append(Var(dom=range(maxTime-tasks_array[i][0]+1), id='start_task'+nbr))
    #priorityVars+="order_task"+nbr+","+"task_machine"+nbr+",start_task"+nbr+","
    #tasks_ends.append(Var(dom=range(maxTime), id='end_task'+str(i)))
#priorityVars=priorityVars[:-1]
satisfy(
    AllDifferent(tasks_order),
    [(If(tasks_order[0]==i, Then = tasks_starts[i]==0) )for i in range(ntasks)], #task 1 start at 0

    [(If(tasks_order[i]+1==tasks_order[j],
         Then = (tasks_starts[j]>=tasks_starts[i]) ) )
         for i in range(ntasks) for j in range(i, ntasks)],# respect the starting order
    #[ ((True))
    # for i in range(ntasks)
    # for j in ressources_incompatibilities[i]],
    #[tasks_ends[i]==tasks_array[i][0]+tasks_starts[i]-1 for i in range(ntasks)],

    [  If(tasks_order[i]<tasks_order[j] ,
        Then=(tasks_array[i][0]+tasks_starts[i]-1 < tasks_starts[j]))
     for i in range(ntasks)
     for j in ressources_incompatibilities[i]],

    [  If(  (tasks_machines[i]==tasks_machines[j])&(tasks_order[i]<tasks_order[j]) ,
        Then=(tasks_array[i][0]+tasks_starts[i]-1 < tasks_starts[j]))
     for i in range(ntasks)
     for j in range(ntasks)],

     
    #[ If(tasks_starts[i]!=0,
    #     Then=Sum((tasks_array[i][0]+tasks_starts[i] == tasks_starts[j] )for j in range(ntasks))>=1)
    # for i in range(ntasks)]
    
    
    #[ If(tasks_order[i]==j,
    #     Then = tasks_ends[j]==max(tasks_array[i][0]+tasks_starts[j])
    #     for i in range(ntasks) for j in range(ntasks)]
)
#if machines_limit>ressources_limit:
#minimize(
#        Maximum(tasks_array[i][0]+tasks_starts[i])
        #calculate_cost(tasks_order, tasks_machines)#, Sum(tasks_order)+Sum(tasks_machines))
#    )

#print(priorityVars)
result=solve(options="-t=60s -p=ESAC3 -varh=Dom")
print(result)
if result in (SAT, OPTIMUM):
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
    for i in range(len(machines_usages)):
        machine=machines_usages[i]
        print(f"M{i}\t{[key for key, value in sorted(machine.items(), key=lambda item: item[1])]}")
#order only
# machines uses
# calculate cost