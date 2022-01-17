# import cv2 as cv

# cam = cv.VideoCapture(0)
# cv.namedWindow("webcamview")
# cv.namedWindow("faceview")
# face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# while True:
#     ret, frame = cam.read();
#     if not ret: 
#         print("frame inlezen mislukt, stop programma")
#         break
#     cv.imshow("webcamview", frame)
#     # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(frame, 1.1, 4)

#     for (x, y, w, h) in faces:
#         cv.rectangle(frame, (200, 120), (450, 300), 0)
#         # Display
#         cv.imshow('faceview', frame)

#     if len(faces) == 1:
#         (x, y, w, h) = faces[0]
#         faceROI = frame[y:(y+h), x:(x+h)]
#         cv.imshow('webcamview', faceROI)
#         cv.rectangle(frame, (x, y), (x + w, y + h), [255,0,0], 2)
#     else:
#         for (x, y, w, h) in faces:
#             cv.rectangle(frame, (x, y), (x + w, y + h), [255,0,0], 2)
    
#     cv.imshow('webcamview', frame)

#     cv.waitKey(1000)
#     #stop programma met 'q' toets
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         cam.release()
#         cv.destroyAllWindows()
#         break


# import cv2 as cv
# import numpy as np

# #face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

# cam = cv.VideoCapture(0)

# cv.namedWindow('webcamview')
# while True:
#     ret, frame = cam.read()
#     if not ret:
#         print('frame inlezen mislukt, stop programma')
#         break
#     # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(frame, 1.1, 4)
#     aantalGezichten = len(faces)
#     for (x, y, w, h) in faces:
#         cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#         # Display
#         cv.imshow('faceview', frame)

#     if len(faces) == 1:
#         (x, y, w, h) = faces[0]
#         faceROI = frame[y:y+h, x:x+w]
#         cv.imshow('faceview', faceROI)
#         cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#     else:
#         for (x, y, w, h) in faces:
#             cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#         cv.imshow('webcamview', frame)

#     # cv.imshow('webcamview', frame)



#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break




# # for (x, y, w, h) in faces:
# #  cv.rectangle(frame, 20, 40, color)
# #  # Display
# #  cv.imshow('faceview', frame)

# cam.release()
# cv.destroyAllWindows()

import cv2 as cv

face_cascade = cv.CascadeClassifier('Week_1\haarcascade_frontalface_default.xml')

cam = cv.VideoCapture(0)
cv.namedWindow('webcamview')

while True:
    ret, frame = cam.read()
    if not ret:
        print('frame inlezen mislukt, stop programma')
        break
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)

    aantalGezichten = len(faces)
    for (x, y, w, h) in faces:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv.imshow('faceview', frame)

    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        faceROI = frame[y:y+h, x:x+w]
        cv.imshow('faceview', faceROI)
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    else:
        for (x, y, w, h) in faces:
            cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv.imshow('webcamview', frame)

    cv.imshow('webcamview', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 6a. Hij detecteert in de meeste houdingen mijn gezicht, alleen soms wat moeite met de zijkant van mijn gezicht
# 6b. Hij detecteert mijn gezicht tijdens verschillende gezichtsuitdrukkingen
# 6c. Bij heel licht en heel donker (als delen van mijn gezicht niet meer te zien zijn) lukt het niet altijd even goed om mijn gezicht te detecteren
# 6d. Als ik mijn ogen bedek met mijn handen detecteert hij mijn gezicht helemaal niet, bij het bedekken van andere delen doet hij er wat langer over maar lukt het meestal wel


cam.release()
cv.destroyAllWindows()