import cv2
import os

cam = cv2.VideoCapture('http://192.168.0.106:8081/')
cam.set(3, 640)
cam.set(4, 480) 
flag, img = cam.read()

cv2.imshow('image', img)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0

while (True):
    ret, img = cam.read()
    if (ret):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #faces = face_detector.detectMultiScale(gray, 1.3, 5)
        faces = face_detector.detectMultiScale(gray, 1.1, 19)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            print(count)

            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        cv2.imshow('image', img)
    else:
        cv2.waitKey(100)
        
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
    elif count >= 150:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
