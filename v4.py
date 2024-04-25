import json
from pycsp3 import *
import matplotlib.pyplot as plt
from matplotlib import patheffects

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
read_input(test_files[0])
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
    tasks_starts.append(Var(dom=range(maxTime-tasks_array[i][0]), id='start_task'+nbr))
    #priorityVars+="order_task"+nbr+","+"task_machine"+nbr+",start_task"+nbr+","
    #tasks_ends.append(Var(dom=range(maxTime), id='end_task'+str(i)))
#priorityVars=priorityVars[:-1]
satisfy(
    AllDifferent(tasks_order),
    [(If(tasks_order[0]==i, Then = tasks_starts[i]==0) )for i in range(ntasks)], #task 1 start at 0
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
minimize(
        Maximum(tasks_array[i][0]+tasks_starts[i])*100+Sum(tasks_starts)
        #calculate_cost(tasks_order, tasks_machines)#, Sum(tasks_order)+Sum(tasks_machines))
)

#print(priorityVars)

def draw_schedule(activities, end, width=15, height=8):
    n_machines=len(activities)
    fig, ax = plt.subplots(figsize=(width, height)) 
    ax.set_xlim(0, end+1)
    ax.set_ylim(0, n_machines + 1)
    for i, activity_line in enumerate(activities, start=1):
        for activity in activity_line:
            start_time = activity['start_time']
            duration = activity['duration']
            end_time = start_time + duration
            ax.plot([start_time, end_time], [i, i], linewidth=20, solid_capstyle='butt')
            text_x = (start_time + end_time) / 2
            text_y = i
            mytxt = ax.text(text_x, text_y, activity['name'], ha='center', va='center', color='white', fontsize=12)
            mytxt.set_path_effects([patheffects.withStroke(linewidth=3, foreground='black')])

    ax.set_yticks(range(1, n_machines + 1))
    ax.set_yticklabels([f'Machine {i}' for i in range(1, n_machines+1)])
    ax.set_xlabel('Time')
    ax.set_title("Tasks execution took "+str(end)+" units of time")
    plt.grid(True)
    plt.show()

result=solve(options="-t=30s -varh=Dom -valh=RunRobin -p=ESAC3")
print(result)
if result in (SAT, OPTIMUM):
    optimal_time=0
    for i in range(len(tasks_array)):
        optimal_time=max(optimal_time,value(tasks_starts[i])+tasks_array[i][0])
    print(f'Execution Time = {optimal_time}')
    machines_usages = [{} for _ in range(len(machines_array))]

    for i in range(len(tasks_array)):
        start = values(tasks_starts)[i]
        str_start = str(start)
        m_indx = value(tasks_machines[i])
        ressource_usage = ""
        for ressource in tasks_array[i][2]:
            ressource_usage+=str(ressource+1)+" "
        if len(ressource_usage)>0:
            ressource_usage=" r["+ressource_usage[:-1]+"]"
        name = f't{i+1}{ressource_usage}, start={str_start}, dur={tasks_array[i][0]}'
        machines_usages[m_indx][name] = start

    activities = []
    for machine in machines_usages:
        machine_activities = []
        for activity, start_time in sorted(machine.items(), key=lambda item: item[1]):
            name, _, _ = activity.split(', ')
            name = name.split('=')[0]  # Extracting the activity name
            start_time = int(start_time)
            duration = int(activity.split(', ')[-1].split('=')[-1])
            machine_activities.append({'name': name, 'start_time': start_time, 'duration': duration})
        activities.append(machine_activities)

    draw_schedule(activities, optimal_time)

# machines uses
# calculate cost