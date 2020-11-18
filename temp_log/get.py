import requests
import json
import sys

supervisor = {"login": "admin"}

login = ""
if len(sys.argv) > 1:
    login = str(sys.argv[1])

response = requests.get("https://alfalfa-project.herokuapp.com/api/auth", json = {"login": login, "password": login})
if (response.status_code != 200):
    print('Ошибка аутентификации')
else:
    token = response.content.decode("utf-8")
    response = requests.get("https://alfalfa-project.herokuapp.com/api/"+ login + "/measurements", headers = {"Bearer": token})
    if(response.status_code != 200):
        print('Ошибка сервера')
    else:
        print(response.content)