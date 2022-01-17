import cv2
import os
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from Email import sendMail

def startFaceRecognition():
    # voert een classsifier uit op de haarcascade xml file, dit is voor de 'gewone' face recognition
    cascPath = os.path.dirname(
        cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    model = load_model("D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Eindproject\mask_recog1.h5") # laadt het model in voor de mask recognition

    video_capture = cv2.VideoCapture(0) # webcam
    i = 0

    while True:
        ret, frame = video_capture.read() # leest de webcam uit
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converteert de frame naar greyscale
        faces = faceCascade.detectMultiScale(gray,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(60, 60),
                                                flags=cv2.CASCADE_SCALE_IMAGE) # hier wordt de classifier gerunt over de frame van de webcam
        faces_list = [] # lijst met gezichten
        preds = [] # lijst met labels
        for (x, y, w, h) in faces:
            face_frame = frame[y:y + h, x:x + w] # maakt een frame aan met alleen het gezicht in de foto
            face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB) # convert colors naar RGB
            face_frame = cv2.resize(face_frame, (224, 224)) # resize image naar 224x224
            face_frame = img_to_array(face_frame) # image naar array
            face_frame = np.expand_dims(face_frame, axis=0) #expand dimensions
            face_frame = preprocess_input(face_frame) # preproces input
            faces_list.append(face_frame) # voeg processed image toe aan de faces_list lijst
            if len(faces_list) > 0: # als er een gezicht aanwezig is: predict
                preds = model.predict(faces_list)
            for pred in preds:
                (mask, withoutMask) = pred
            label = "Mask" if mask > withoutMask else "No Mask" # labels voor de in de image --> draagt een masker: krijgt label Mask en andersom
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100) # het label met hoeveel procent zekerheid de prediction is, afgerond om 2 decimalen
            cv2.putText(frame, label, (x, y - 10), # locatie, font en kleur van de text
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

            if cv2.waitKey(1) & 0xFF == ord('s'): # op het moment dat "s" wordt ingedrukt in de window wordt er een capture gemaakt.
                return_value, image = video_capture.read()
                path_metMasker = "D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Eindproject\metMasker" # path naar foto's met masker
                path_zonderMasker = "D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Eindproject\zonderMasker" # path naar foto's zonder masker
                i += 1
                if mask > withoutMask: # hier wordt de foto die gemaakt is als bestand opgeslagen is de desbetreffende map onder de naam "mask_{nummer}.jpg"
                    cv2.imwrite(os.path.join(path_metMasker, f"mask_{i}.jpg"), image)
                    cv2.imshow("Photo with facemask", image)
                elif withoutMask > mask: # hier wordt de foto die gemaakt is als bestand opgeslagen is de desbetreffende map onder de naam "no_mask_{nummer}.jpg"
                    cv2.imwrite(os.path.join(path_zonderMasker, f"no_mask_{i}.jpg"), image)
                    cv2.imshow("Photo without facemask", image)
                else: 
                    cv2.imshow("Nothing to see here", image) # als er geen gezicht gedetecteerd wordt in het frame als er een foto wordt gemaakt zie je alleen de foto in een frame genaamd "Nothing to see here"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2) # de rectangle die over het gezicht heen gaat op het moment van detecteren van een gezicht
        cv2.imshow('Video', frame) # het frame waar alles in plaats vindt.
        if cv2.waitKey(1) & 0xFF == ord('q'):  # als 'q' ingedrukt wordt in het frame sluit het frame
            break
    
    # cleanup
    video_capture.release()
    cv2.destroyAllWindows()