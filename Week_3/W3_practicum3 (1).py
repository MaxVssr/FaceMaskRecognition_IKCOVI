#!/usr/bin/env python

"""
Dit script is onderdeel van de standaard scripts
voor de module ikcovi van de HS Leiden
"""
import os
import cv2 as cv
import numpy as np
import face_recognition

__author__ = "Alize Pistidda"
__copyright__ = "Copyright 2021, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"

#PAS DEZE VARIABELEN AAN NAAR JOUW SITUATIE
base_folder = 'D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_3'
naam = "Max"
# naam = "Froke"
kleur_wit = [255, 255, 255]

# laat alleen de gevonden gezichten zien als deze boolean op true staat:
show_frame = False

#alle gegenereerde files worden in deze folder 'base_folder/naam/' weggeschreven
output_folder = os.path.join(base_folder,naam)
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

detectie_pogingen = 0;

cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        break

    #computers gebruiken geen kleur voor hun detectie
    #en grijswaardes rekenen sneller
    # je kan deze regel gebruiken maar het hoeft niet:
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('webcam', frame)

    # als je op spatie drukt, moet jouw gezicht via face recognition worden gevonden
    if cv.waitKey(1) & 0xFF == ord(' '):

        detectie_pogingen += 1

        # schrijf alvast het originele beeld weg
        basis = os.path.join(output_folder, "frame_" + str(detectie_pogingen));
        cv.imwrite(basis + ".png", frame)

        # haalt de bounding boxes van de gezichten op
        # telt hoeveel gezichten er in het plaatje zijn gevonden
        face_bounding_boxes = face_recognition.face_locations(frame)
        nr_gezichten = len(face_bounding_boxes)
        print(f"er zijn {nr_gezichten} gezichten gevonden")

        #features en ROI wegschrijven deze loop gaan we alleen in als er een face feature is gevonden
        for i, (top, right, bottom, left) in enumerate(face_bounding_boxes):
            # zorg dat alle gezichten onder een andere naam worden opgeslagen:
            base = basis + "_" + str(i);

            # haal de ROI van het gezicht op
            # schrijf nu het png plaatje
            x1 = left
            y1 = top
            x2 = right
            y2 = bottom

            roi_gezicht = frame[y1:y2, x1:x2]
            cv.imwrite(base + "_gezicht.png", roi_gezicht)

            # zoek de gezichtsfeatures voor de boundingbox
            # Normaliseer de gezichten (zet alle gezichten met de neus naar voren)
            # bereken de 128 afstanden tussen de verschillende gezichtspunten.
            #  schrijf de lijst met features weg voor later gebruik bij classificatie
            feature_list = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]
            np.save(base + '_feature.npy', feature_list)

            # laat alleen het resultaat frame zien als er om gevraagd wordt:
            if show_frame:
                face_landmarks = face_recognition.face_landmarks(frame, [(top, right, bottom, left)])

                for structure, punten in face_landmarks.items():
                    for punt in punten:
                        cv.circle(frame, punt, 2, kleur_wit, 1)

                cv.imshow("resultaat", frame);

    #waitkey(1) geeft 1 de character code terug die is ingedrukt en -1 als niks is ingedrukt
    #& 0xFF is een binary AND operatie om ervoor te zorgen dat een alleen single byte ASCII representatie van de aangeslagen key overblijt.
    # cv.ord(<char>) geeft de ascii representatie terug van de q.
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()