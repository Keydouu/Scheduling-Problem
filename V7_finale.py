import json
from pycsp3 import *
import matplotlib.pyplot as plt
from matplotlib import patheffects

#for filename in os.listdir("."):
#        if filename.endswith(".log"):
#            os.remove("./"+filename)

def draw_schedule(activities, end):
    n_machines=len(activities)
    fig, ax = plt.subplots()
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
    ax.set_title("Tasks execution took "+str(end)+" unit of time")
    plt.grid(True)
    plt.show()

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
    
test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[2])
ntasks=len(tasks_array)
greedyOrder = sorted(range(ntasks), key=lambda i: (-tasks_array[i][0], len(tasks_array[i][1])))
print(f'init : {greedyOrder}')
ntasks=len(tasks_array)
nMachines=len(machines_array)
# ------------------------------------------------------ N E W ------------------------------------------------------

def allDifferentMachines(tasks_indexs, new_task):
    clear()
    tasks_indexs.add(new_task)
    if len(tasks_indexs)==1:
        return True
    tasks_machines = []
    for index in tasks_indexs:
        tasks_machines.append(Var(dom=set(tasks_array[index][1]), id='task_machine'+str(index)))
    satisfy(
        AllDifferent(tasks_machines)#using pycsp to check if all task can be executed on different valid machines
    )
    result = solve()
    if result != SAT:
        tasks_indexs.remove(new_task)
        return False
    return True

def orderGenerator():
    greedy_order = sorted(range(ntasks), key=lambda i: (-tasks_array[i][0], -len(tasks_array[i][1]), len(tasks_array[i][2])))#order by higher length,
                                                                #then higher number of available machines, then lower number of needed ressources
    #print(greedy_order)
    my_batches=[]
    old_tabu_ressources = set([i for i in range(n_ressources)])
    updated_machines_number=nMachines
    ressources_users=[] # [ressource number]
    non_ressources_users=[]
    while True:#go greedy when you're done assigning ressource I guess ?
        tabu_ressources = set()
        current_batch = set()
        #machines_usage=[0 for _ in range(nMachines)]
        updated_ressources_number=len(old_tabu_ressources)
        ressources_users.append([None for _ in range(n_ressources)])
        iteration = len(ressources_users)-1
        for tasks_index in greedy_order:
            if len(tabu_ressources)==updated_ressources_number:
                break
            if len(tasks_array[tasks_index][2])>0:
                if(tabu_ressources.isdisjoint(tasks_array[tasks_index][2])):
                    if allDifferentMachines(current_batch, tasks_index):
                        for ressource in tasks_array[tasks_index][2]:
                            tabu_ressources.add(ressource)
                            ressources_users[iteration][ressource]=tasks_index
                            
        
        #if len(tabu_ressources)==0:
        if len(greedy_order)==0:
            break
        old_tabu_ressources=tabu_ressources

        greedy_order = [x for x in greedy_order if x not in current_batch]
        non_ressources_users.append([])

        for tasks_index in greedy_order:
            if len(current_batch)==updated_machines_number:# gain time, but maybe condition is kinda fucked up because of some task being denied entry to the batch due to ressources incompatibilities ?
                    break
            if(tabu_ressources.isdisjoint(tasks_array[tasks_index][2])):
                if allDifferentMachines(current_batch, tasks_index):
                    non_ressources_users[iteration].append(tasks_index)
                
        greedy_order = [x for x in greedy_order if x not in current_batch]

        updated_machines_number=len(current_batch)
        #print(f"{current_batch}|{greedy_order}")
        my_batches.append(current_batch)
    if len(greedy_order)>0:
        my_batches.append(greedy_order)
    return my_batches, ressources_users, non_ressources_users

all_batches, ressources_users, non_ressources_users = orderGenerator()

def link_values_pairwise(arrays):
    result = {}
    for i in range(0, len(arrays) - 1):
        array1 = arrays[i]
        array2 = arrays[i + 1]
        for val1, val2 in zip(array1, array2):
          if val2 is not None:
            result[val2] = []
            if val1 is not None :
                result[val2].append(val1)
    return result

ressource_links_map = link_values_pairwise(ressources_users)

clear()
print(f"all batches {all_batches}")
print(f"ressource users {ressources_users}")
print(f"non ressources users {non_ressources_users}")
tasks_machines = [None for _ in range(ntasks)]
tasks_starts= [None for _ in range(ntasks)]
worst=1
all_batches_min = all_batches_max = 0
for batch in all_batches:
    current_min = current_max = 0
    tmp = []
    for index in batch:
        current_min = min(current_min, tasks_array[index][0])
        current_max = max(current_max, tasks_array[index][0])
        tasks_machines[index]=Var(dom=set(tasks_array[index][1]), id='task_machine'+str(index))
        tasks_starts[index]=Var(dom=range(all_batches_min,all_batches_max+1), id='start_task'+str(index))
        tmp.append(tasks_machines[index])
    satisfy(
        AllDifferent(tmp)
    )
    all_batches_min+=current_min
    all_batches_max+=current_max


score = Var(dom=range(all_batches_min, all_batches_max+1))
satisfy(
    [tasks_starts[i]==0 for i in all_batches[0]],

    [ If(tasks_machines[current_index]==tasks_machines[previous_index],
         Then=tasks_starts[current_index]==tasks_starts[previous_index]+tasks_array[previous_index][0])
     for current_batch in range(1, len(all_batches))
     for current_index in non_ressources_users[current_batch]
     for previous_index in all_batches[current_batch-1]],

     #[ If(tasks_machines[current_index]==tasks_machines[previous_index],
     #    Then=tasks_starts[current_index]==
     #    Maximum([tasks_starts[previous_index]+tasks_array[previous_index][0],
     #       Maximum(ressources_users[current_batch-1][ressource] for ressource in tasks_array[current_index][2])]))
     #for current_batch in range(1, len(all_batches))
     #for current_index in ressources_users[current_batch]
     #for previous_index in all_batches[current_batch-1]],

    score==Maximum((tasks_starts[i]+tasks_array[i][0])
                for i in range(ntasks))
)

def link_values(array1, array2):
    result = {}
    added_values = set()  # To keep track of added values

    for val2, val1 in zip(array2, array1):
        if val1 is not None and val1 not in added_values:
            if val2 not in result:
                result[val2] = []
            result[val2].append(val1)
            added_values.add(val1)

    return result


for ressource_users_batch in range(1, len(ressources_users)):
    for key in ressources_users[ressource_users_batch]:
        if key == None:
            continue
        element_values = ressource_links_map[key]
        if len(element_values)>0:
            satisfy(
                [If(tasks_machines[key]==tasks_machines[previous_index],
                    Then=tasks_starts[key]==
                    Maximum(tasks_starts[previous_index]+tasks_array[previous_index][0],
                        [tasks_starts[new_ressource]+tasks_array[new_ressource][0]
                                for new_ressource in element_values]))
                for previous_index in all_batches[ressource_users_batch-1]],
                
                [tasks_starts[key]>=tasks_starts[new_ressource]+tasks_array[new_ressource][0]
                for new_ressource in element_values]#juuuust in the unlikely case a macine was not used at all in previous batch
            )
        else :
            satisfy(
                [ If(tasks_machines[key]==tasks_machines[previous_index],
                    Then=tasks_starts[key]==tasks_starts[previous_index]+tasks_array[previous_index][0])
                for previous_index in all_batches[ressource_users_batch-1]]
            )
minimize(
    score
)

result = solve(options="-t=120s")
print(result)

if result in (SAT, OPTIMUM): #drawing the result
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
            ressource_usage+="r"+str(ressource+1)+" "
        if len(ressource_usage)>0:
            ressource_usage=" ["+ressource_usage[:-1]+"]"
        name = f't{i+1}{ressource_usage}, start_time={str_start}, duration={tasks_array[i][0]}'
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
        #print(machine_activities)
    draw_schedule(activities, optimal_time)