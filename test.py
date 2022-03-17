import requests
import json
import ast

tasks = requests.get(
    'https://yy-todobot.herokuapp.com/api/v1/todo/task', headers={'Authorization': f"Bearer {'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2MjJkOTllZmJiZGY1MTFhZmNkZTMxNzYiLCJ1c2VybmFtZSI6ImpvaG4iLCJpYXQiOjE2NDczMzE3MjEsImV4cCI6MTY0OTkyMzcyMX0.Atu6GdksuroZMTpqiIWB1GDsoecewONq5vZtKiJSTMU'}"})
tasks = json.loads(tasks.content.decode('utf-8'))
allTask = tasks['todo'][::-1]
print(type(allTask[0]))

delVal = ['test', 'chicken', 'fish']


def getID(task):
    for i in delVal:
        if(i == task['task']):
            return task['_id']


x = map(getID, allTask)
x = [j for j in list(x) if j]
print(x)
