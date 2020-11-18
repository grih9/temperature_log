#import requests
#import json
#import datetime

#login = "admin"
#password = "admin"

#response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": "admin", "password": "123"})
#print(response.status_code)

#supervisor = {"login": "admin"}

#timeNow = datetime.datetime.now().isoformat()
#print(str(timeNow)[0:-3] + "Z")
import requests
import json
import sys

supervisor = {"login": "admin"}

login = ""
if len(sys.argv) > 1:
    login = str(sys.argv[1])
    response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": login, "password": login,})
    if(response.status_code != 200):
        print('Ошибка сервера')
    else:
        print('Зарегистрирован')
else:
    print('Ошибка ввода')
#response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": "grih9", "password": "grih9",})
#print(response.status_code)

#response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": "whoopzee", "password": "whoopzee"})
#print(response.status_code)

#response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": "kir0108", "password": "kir0108"})
#print(response.status_code)

#response = requests.post("https://alfalfa-project.herokuapp.com/api/register", json = {"login": "daniilXT", "password": "daniilXT"})

