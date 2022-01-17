#!/usr/bin/env python

"""
Dit script is onderdeel van de standaard scripts
voor de module ikphbv van de HS Leiden

We gaan nieuwe gezichten via de webcam inlezen.

Hiervoor trainen we de computer met een  Support Vector Machine
op basis van trainingsdata. Deze trainingsdata zit
in  een trainingsdirectory die er zo uitziet:

Structure:
        <student_data>/
            <naam_student_1>/
                frame_1.png
                frame_2.png
                .
                .
                frame_n..png
           <naam_student_2>/
               frame_1.png
               frame_2..png
                .
                .
               frame_n.png
            .
            .
            <naam_student_n>/
               frame_1.png
               frame_2.png
                .
                .
               frame_n.png
"""

import re
import os
import pickle
import face_recognition
from sklearn import svm

__author__ = "Alize Pistidda"
__copyright__ = "Copyright 2020, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"

# hierin staan al onze folders met studentnamen
student_data = 'D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Week_4\gezichten'

#initialiseer alvast de SVM:
features = []
namen = []

# we lopen nu door de folders met student data
for student in os.listdir(student_data):
    print("Begin verwerken student {} ".format(student))

    #Maak het path voor de  directory voor deze student om de foto's op te halen
    fotodir = os.path.join(student_data, student)
    if not os.path.isdir(fotodir):
        continue

    # we zijn nu geïnteresseerd in de frames in de student fotodir folder
    # Dit commando haalt alle foto's op en geeft dmv een  regexpressie alleen de hele frames terug
    frames = [f for f in os.listdir(fotodir) if re.match(r'frame_\d+\.png', f)]

    #nu gaan we een voor een door de lijst met frames heen:
    #   1. we halen de features eruit
    #   2. als dat gelukt is, en er is precies 1 gezicht gevonden:
    #      doe een face encoding (normaliseer het gezicht en bepaal de belangrijkste afstanden)
    #   3. sla het bijbehorende label op
    for foto in frames:
        print("Foto " + foto + " van Student " + student)
        fotofile = os.path.join(fotodir, foto)

        #laten we alvast een feature file maken waar we de gedetecteerde features opslaan.
        #dit proces duurt lang en willen we niet te vaak herhalen.
        feature_file = fotofile.replace(".png", "_features.txt")

        gezicht = face_recognition.load_image_file(fotofile)
        face_bounding_boxes = face_recognition.face_locations(gezicht)

        if len(face_bounding_boxes) == 1:
            gezichts_afstanden = face_recognition.face_encodings(gezicht)[0]
            features.append(gezichts_afstanden)
            namen.append(student)

        with open(feature_file, "w") as outfile:
            for val in gezichts_afstanden:
                outfile.write(str(val) + "\n")

        #de features zijn al berekend, lees ze in en ga naar de volgende file
        if os.path.isfile(feature_file):
            feature_lijst = open(feature_file).read().splitlines()
            features.append(feature_lijst)
            namen.append(student)
            continue



print("Trainingsdata samenvatting :")
print(str(len(os.listdir(student_data))) + " personen ")
print(str(len(namen)) + " labels ")
print(str(len(features)) + " feature vectoren")

classifier = svm.SVC(gamma='scale')
classifier.fit(features, namen)
with open(os.path.join(student_data, 'saved_model.pickle'), 'wb') as handle:
 pickle.dump(classifier, handle)