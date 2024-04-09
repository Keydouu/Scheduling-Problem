import json
from pycsp3 import *

machines_array = []
tasks_array = []
worst_time_possible=0
def read_input(input_file):
    file = open(input_file)
    file_data = json.load(file)
    for i in range (int(file_data['nMachines'])):
        machines_array.append(i)
    for task in file_data['tests']:
        tasks_array.append(Task(task['duration'], task['machines'], task['resources']))
        worst_time_possible+=task['duration']

class Task:
    def __init__(self, duration, machines=[], ressources=[]):
        self.duration = duration
        self.ressources = ressources
        self.machines = machines
        if len(self.machines)==0:
            self.machines=machines_array
    def getConsumedTask(self):
        if self.duration>0:
            return Task(self.duration-1, self.machines, self.ressources)
        return self
    def getDuration(self):
        return self.duration

tasks_ends = VarArray(size=[len(tasks_array)])
time_table = VarArray(size=[len(machines_array)][worst_time_possible])
satisfy(
    Count(time_table)
)
minimize(
    max(tasks_ends)
)