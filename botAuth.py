from ast import Try
from wsgiref import headers
import requests
import json


class BotAuth():
    def __init__(self):
        pass

    def login(self, credentialsDict):
        loginDetails = requests.post(
            'https://yy-todobot.herokuapp.com/api/v1/todo/auth/login', json=credentialsDict)
        loginOutcome = json.loads(
            loginDetails.content.decode('utf-8'))

        try:
            self.token = loginOutcome['token']
        except KeyError:
            return "Wrong username or password"

        return self.token

    def register(self, credentialsDict):
        registerDetails = requests.post(
            'https://yy-todobot.herokuapp.com/api/v1/todo/auth/register', json=credentialsDict)
        registerOutcome = json.loads(
            registerDetails.content.decode('utf-8'))

        try:
            self.token = registerOutcome['token']
        except KeyError:
            return 'User already exists'

        return self.token


class BotMethods():
    def __init__(self):
        pass

    def allTasks(self, jwt):
        tasks = requests.get(
            'https://yy-todobot.herokuapp.com/api/v1/todo/task', headers={'Authorization': f"Bearer {jwt}"})
        tasks = json.loads(tasks.content.decode('utf-8'))
        allTask = tasks['todo'][::-1]

        def getTask(task):
            date = task['date'].split('T')[0]
            return task['task'] + " " + date + '\n'

        return list(map(getTask, allTask))

    def createTask(self, jwt, newTaskDict):
        addTask = requests.post(
            'https://yy-todobot.herokuapp.com/api/v1/todo/task', json=newTaskDict, headers={'Authorization': f"Bearer {jwt}"})
        addTask = json.loads(addTask.content.decode('utf-8'))
        return addTask

    def tasksOnly(self, jwt):
        tasks = requests.get(
            'https://yy-todobot.herokuapp.com/api/v1/todo/task', headers={'Authorization': f"Bearer {jwt}"})
        tasks = json.loads(tasks.content.decode('utf-8'))
        tasks = tasks['todo'][::-1]

        return tasks

    def removeTasks(self, jwt, delValList):
        tasks = requests.get(
            'https://yy-todobot.herokuapp.com/api/v1/todo/task', headers={'Authorization': f"Bearer {jwt}"})
        tasks = json.loads(tasks.content.decode('utf-8'))
        tasks = tasks['todo'][::-1]

        def getID(task):
            for i in delValList:
                if(i == task['task']):
                    return task['_id']

        idList = list(map(getID, tasks))
        # Using list comprehension to remove the "None" values in the idList above.
        idList = [j for j in list(idList) if j]

        for id in idList:
            requests.delete(
                f'https://yy-todobot.herokuapp.com/api/v1/todo/task/{id}', headers={'Authorization': f'Bearer {jwt}'})
    
        