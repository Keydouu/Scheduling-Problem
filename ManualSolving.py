import json
from itertools import permutations
from copy import deepcopy

machines_array = []
tasks_array = []
lengths=[]
n_ressources=0
def read_input(input_file):
    file = open(input_file)
    file_data = json.load(file)
    global n_ressources
    n_ressources=file_data['nResources']
    for i in range (int(file_data['nMachines'])):
        machines_array.append(i)
    for task in file_data['tests']:
        lengths.append(int(task['duration']))
        if len(task['machines'])>0:
            tasks_array.append([int(task['duration']), task['machines'], task['resources']])
        else:
            tasks_array.append([int(task['duration']), machines_array, task['resources']])
    
test_files=['./t10-example.json', './t20m10r3-1.json', './t40m10r3-2.json']
read_input(test_files[1])
def get_worst_time(indexs):
    ressources_min_times=[0 for _ in range(n_ressources)]
    machine_times_any=[]
    machines_min_times=[0 for _ in range(len(machines_array))]
    for index in indexs:
        task=tasks_array[index]
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
    #print(f'R{ressources_limit} - M{machines_limit} ')
    return ressources_limit, machines_limit, max({ressources_limit, machines_limit})

ntasks=len(tasks_array)
nMachines=len(machines_array)
ressources_limit, machines_limit, maxTime = get_worst_time(range(ntasks))

def printSol(sol):#task id - machine - start time
    global fullRange
    machines_usages=[{} for _ in range(len(machines_array))]
    for i in sol:
        task=i[0]
        start=i[2]
        str_start=str(start)
        machines_usages[i[1]]['s'+str_start+' t'+str(task)+' d'+str(tasks_array[task][0])+ ' e'+str(start+tasks_array[task][0]-1)]=start
    for machine in machines_usages:
        #machine.sort()
        print([key for key, value in sorted(machine.items(), key=lambda item: item[1])])

#fullRange=sorted(range(ntasks), key=lambda i: lengths[i], reverse=True)

fullRange = sorted(range(ntasks), key=lambda i: (len(tasks_array[i][1]), -len(tasks_array[i][2]),  -tasks_array[i][0]))
winning_Combination = []

def valuePicker(vars, machines_free, valid_machines_indexs, lastIndex=0):
    indexReset=len(vars)
    ordered_indices = sorted(range(len( machines_free)), key=lambda i: machines_free[i], reverse=True)
    while len(valid_machines_indexs)>0:
        current_machine_index=ordered_indices[0]
        if not current_machine_index in valid_machines_indexs:
            ordered_indices.pop()
            continue
        taskIndex=lastIndex+1
        while taskIndex!=lastIndex:
            if taskIndex==indexReset:
                taskIndex=0
            if current_machine_index in vars[taskIndex][1]:
                vars[taskIndex][1].remove(current_machine_index)
                return taskIndex, current_machine_index, valid_machines_indexs
            taskIndex+=1
        valid_machines_indexs.remove(current_machine_index)#FALSE FALSE FALSE
    return -1, -1, None
        

def tryCombinations(ressources_free, machines_free, currentBest, unassigned_tasks_indexs, current_sol, latest_start=0):
    #case we're done
    if len(unassigned_tasks_indexs)==0:#save result
        global winning_Combination
        winning_Combination = deepcopy(current_sol)
        newScore=max(machines_free)-1
        print(f"new score = {newScore}")
        #printSol(winning_Combination)
        if(newScore==ressources_limit-1):#Optimum for sure, exit all
            print("optimum")
            return True, True, newScore
        return False, True, newScore
    
    ressources_changes=[]
    machines_changes=0
    newUnassigned = deepcopy(unassigned_tasks_indexs)
    local_improved=False
    
    okay_machines_index=deepcopy(machines_array)
    assignements=[i, deepcopy(tasks_array) for i in unassigned_tasks_indexs]
    
    for current_task_index in unassigned_tasks_indexs:
        newUnassigned.remove(current_task_index)
        task_length=tasks_array[current_task_index][0]
        
        for current_machine in tasks_array[current_task_index][1]:
            #cheking start / end time
            start_time=machines_free[current_machine]
            for ressource in tasks_array[current_task_index][2]:
                start_time=max(start_time, ressources_free[ressource])
            end_time=start_time+task_length-1

            #skip the rest if there is no improvement OR if the given order is not respected
            if end_time>=currentBest or start_time<latest_start:
                #if end_time>=currentBest:
                #    print(f"back tracking at score {end_time}")
                continue
            _,_,c=get_worst_time(unassigned_tasks_indexs)
            if c+start_time>currentBest:
                #print("filtered")
                continue
            #update availabilities for machines and ressources
            for ressource in tasks_array[current_task_index][2]:
                ressources_changes.append([ressource, ressources_free[ressource]])
                ressources_free[ressource]=end_time+1
            machines_changes=machines_free[current_machine]
            machines_free[current_machine]=end_time+1


            #reccurence toward next variables
            current_sol.append([current_task_index, current_machine, start_time])#task id - machine - start time
            #print(f"{len(unassigned_tasks_indexs)}-{len(newUnassigned)}")
            #if len(newUnassigned)==0:
            #    printSol(current_sol)
            exit, improved, newBest = tryCombinations(ressources_free, machines_free, currentBest, newUnassigned, current_sol, start_time)
            
            if exit:
                return True, None, None
            if improved:
                local_improved=True
                currentBest = newBest
            #cancel Changes
            current_sol.pop()
            for _ in tasks_array[current_task_index][2]:
                change=ressources_changes[-1]
                ressources_free[change[0]]=change[1]
                ressources_changes.pop()
                del change
            machines_free[current_machine]=machines_changes
        newUnassigned.append(current_task_index)
    return False, local_improved, currentBest

print(f"variables ordering : {fullRange}")
_, _, myResult = tryCombinations([0 for _ in range(n_ressources)], [0 for _ in range(nMachines)], maxTime+100, fullRange, [])    
printSol(winning_Combination)#task id - machine - start time