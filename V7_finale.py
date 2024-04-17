import json
from pycsp3 import *
from matplotlib import plt
def draw_schedule(activities):
    n_machines=len(activities)
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(activity['start_time'] + activity['duration'] + 1 for activity_line in activities for activity in activity_line))
    ax.set_ylim(0, n_machines + 1)
    for i, activity_line in enumerate(activities, start=1):
        for activity in activity_line:
            start_time = activity['start_time']
            duration = activity['duration']
            end_time = start_time + duration
            ax.plot([start_time, end_time], [i, i], linewidth=20, solid_capstyle='butt')
            text_x = (start_time + end_time) / 2
            text_y = i
            ax.text(text_x, text_y, activity['name'], ha='center', va='center', color='white', fontsize=12)

    ax.set_yticks(range(1, n_machines + 1))
    ax.set_yticklabels([f'Machine {i}' for i in range(1, n_machines+1)])
    ax.set_xlabel('Time')
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

tasks_machines = []
tasks_starts= []
worst=1
for i in range(ntasks):
    j=greedyOrder[i]
    tasks_machines.append(Var(dom=set(tasks_array[j][1]), id='task_machine'+str(j)))
    tasks_starts.append(Var(dom=range(0,worst), id='start_task'+str(j)))
    worst+=tasks_array[j][0]

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

result = solve(options="-t=240s -varh=Dom")
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
        name = f't{i+1}, start_time={str_start}, duration={tasks_array[i][0]}'
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

    draw_schedule(activities)