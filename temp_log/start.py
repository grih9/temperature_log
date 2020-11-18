import serial
import time
import datetime
import cv2
import requests
import json

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

while True:
    read_ser=ser.readline()
    if(read_ser.decode("utf-8")[0:-2] == "start"):
        flag = True
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')  # load trained model
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # iniciate id counter, the number of persons you want to include
        id = 7  # two persons (e.g. Jacob, Jack)
        names = ['', 'Фирсов Даниил Анатольевич', 'Бубляев Алексей Вячеславович', 'Коршунов Кирилл Владимирович', 'Толстиков Григорий Николаевич', 'Крайнов Александр Константинович',
                 'ALEXANDR']  # key in names, start from the second place, leave first empty   
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture('http://192.168.0.106:8081/')
        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        count = 0
        counter1 = {2 : 0, 3 : 0, 4 : 0, 5 : 0, 'unknown' : 0}
        counter2 = {2 : 0, 3 : 0, 4 : 0, 5 : 0, 'unknown' : 0}
        logins = {names[1]: "daniilXT", names[2]: "whoopzee", names[3]: "kir0108", names[4]: "grih9", names[5]: "alexandr"}
        confidAvg = 0
        
        while count < 30:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )
            
            for (x, y, w, h) in faces:
                print('Processing')
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    confidence = "  {0}".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}".format(round(100 - confidence))
                counter1[id] += 1
                counter2[id] += int(confidence)
                count = count + 1
            #cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            #cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        #cv2.imshow('camera', img)
        #k = cv2.waitKey(2) & 0xff  # Press 'ESC' for exiting video
        #if k == 27:
            #break
        # Do a bit of cleanup
        #print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        
        maxValue = max(counter1.values())
        maximumID = 0
        for elem in counter1:
            if counter1[elem] == maxValue:
                maximumID = elem
                break
        confidAvg = counter2[maximumID] / counter1[maximumID]
        if (maxValue < 30 or maximumID == "unknown"):
            print('Недостаточно совпадений.' + 'Наиболее подходящий ' + str(names[maximumID]) + ' confidence = ' + str(int(confidAvg)) + ' ' + str(maxValue) + "/30")
            print('Человек распознан верно? y-Да n-Нет')
            a = str(input())
            while (a != 'y' and a != 'n'):
                a = str(input())
            if a == 'y':
                login = logins[names[maximumID]]
                response = requests.get("https://alfalfa-project.herokuapp.com/api/auth", json = {"login": login, "password": login})
                if (response.status_code != 200):
                    print('Ошбика аутентификации')
                    flag = False
                    token = ""
                else:
                    token = response.content.decode("utf-8")
            else:
                counter1[maximumID] = 0
                maxValue = max(counter1.values())
                maximumID = 0
                for elem in counter1:
                    if counter1[elem] == maxValue:
                        maximumID = elem
                        break
                confidAvg = counter2[maximumID] / counter1[maximumID]
                maxValue = max(counter1.values())
                print('Может быть это ' + str(names[maximumID]) + ' confidence = ' + str(int(confidAvg)))
                print('Человек распознан верно? y-Да n-Нет')
                a = str(input())
                while (a != 'y' and a != 'n'):
                    a = str(input())
                if a == 'y':
                    login = logins[names[maximumID]]
                    response = requests.get("https://alfalfa-project.herokuapp.com/api/auth", json = {"login": login, "password": login})
                    if (response.status_code != 200):
                        print('Ошбика аутентификации')
                        flag = False
                        token = ""
                    else:
                        token = response.content.decode("utf-8")
                else:
                    flag = False
                    token = ""
                    login = ""
        elif (confidAvg >= 50 and maxValue == 30):
            print('name = ', names[maximumID], ' confidence = ', int(confidAvg), ' ', maxValue,'/30')
            login = logins[names[maximumID]]
            response = requests.get("https://alfalfa-project.herokuapp.com/api/auth", json = {"login": login, "password": login})
            if (response.status_code != 200):
                print('Ошбика аутентификации')
                flag = False
                token = ""
            else:
                token = response.content.decode("utf-8")
        else:
            print('Человек распознан верно? y-Да n-Нет')
            a = str(input())
            while (a != 'y' and a != 'n'):
                a = str(input())
            if a == 'y':
                login = logins[names[maximumID]]
                response = requests.get("https://alfalfa-project.herokuapp.com/api/auth", json = {"login": login, "password": login})
                if (response.status_code != 200):
                    print('Ошбика аутентификации')
                    flag = False
                    token = ""
                else:
                    token = response.content.decode("utf-8")
            else:
                print('Низкий уровень распознавания.' + 'Наиболее подходящий ' + str(names[maximumID]) + ' confidence = ' + str(int(confidAvg)) + ' ' + str(maxValue) + "/30")
                flag = False
                token = ""
                login = ""
        
    if(read_ser.decode("utf-8")[0:7] == "SumReal"):
        temp = read_ser.decode("utf-8")[9:-2]
        print(temp)
        timeNow = str(datetime.datetime.now().isoformat())[0:-3] + "Z"
        if (token != "" and float(temp) > 35 and float(temp) < 43):
            response = requests.post("https://alfalfa-project.herokuapp.com/api/" + login + "/measurements", json = {"temperature": float(temp), "timestamp": timeNow}, headers = {"Bearer" : token})
            if response.status_code != 200:
                print('Ошибка сервера')
                flag = False
        else:
            flag = False
        ser.open
        if (flag):
            ser.write(b'ok')
        else:
            ser.write(b'not ok')
        ser.close
        