#!/usr/bin/env python

"""
Dit script is onderdeel van de standaard scripts
voor de module ikphbv van de HS Leiden

We gaan nieuwe gezichten via de webcam inlezen
en vergelijken met ons model dat getraind is op
gezichten van studenten van de module ikphbv
"""

import re
import os
import pickle
import cv2 as cv
import face_recognition
from sklearn import svm

__author__ = "Alize Pistidda"
__copyright__ = "Copyright 2020, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"

# hierin staan al onze folders met studentnamen
student_data = 'D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_4/gezichten'
kleur_rood = [0,0,255]
kleur_wit = [255,255,255]

#laten we een frame ophalen van de webcam en deze classificieren:
cap = cv.VideoCapture(0)

# HIER GAAN WE DE CLASSIFIER INLADEN MET PICKLE

with open(os.path.join(student_data, 'saved_model.pickle'), 'rb') as handle:
    classifier = pickle.load(handle)



while True:

    #het algoritme is traag,d us laten we elke 2 seconden een nieuw frame pakken:
    cv.waitKey(2000)

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        break

    #laten we dit bovenaan zetten
    #als we geen gezicht vinden, komen we in elk geval bij deze code.
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    # DETECTEER NU EEN GEZICHT IN HET FRAME
    face_bounding_boxes = face_recognition.face_locations(frame)
    #als we geen gezichten kunnen vinden, dan zijn we klaar
    if len(face_bounding_boxes) == 0:
        cv.imshow('webcam', frame)
        continue

    #we hebben dus gezichten kunnen vinden.
    # Het kan best zijn dat we meerdere gezichten voor de webcam hebben
    # daarom gaan we dus in een for-loop alle gezichten langs
    for i, (top, right, bottom, left) in enumerate (face_bounding_boxes):
        #1. Detecteer de features van het nieuwe gezicht
        gezichts_afstanden = face_recognition.face_encodings(frame)[0]

        #2. Voorspel wie dit is
        naam = classifier.predict([gezichts_afstanden])[0]

        # teken een vierkant om he gezicht
        cv.rectangle(frame, (left, top), (right, bottom), kleur_rood, 2)
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), kleur_rood, cv.FILLED)

        #teken de witte tekst op een donkere achtergrond
        cv.putText(frame, naam, (left + 6, bottom - 6), cv.FONT_HERSHEY_DUPLEX, 1.0, kleur_wit, 1)

        cv.imshow('webcam', frame)


#FEEST IS VOORBIJ: OPRUIMEN MAAR
cap.release()
cv.destroyAllWindows()