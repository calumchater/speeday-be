import requests
import datetime

from getpass import getpass

endpoint = 'http://127.0.0.1:8000/auth/'
# password = getpass()

auth_response = requests.post(endpoint, json={"username": 'calum', "password": 'M21Supressed&!'})
print(auth_response.json())

token = auth_response.json()['token']

endpoint = 'http://127.0.0.1:8000/tasks'

headers = {'Authorization': f'Bearer {token}'}

get_response = requests.post(endpoint, headers=headers, data={"task_name": 'suck_it', "start_time": '2024-01-23', "end_time": '2024-01-24', 'user_id': 1})

print(get_response.json())