import cv2 as cv
import numpy as np
import argparse
import time

#deze functie initialiseert het yolo algoritme en laad het neurale netwerk
def load_yolo():
    # het laden van de gewichten en configuratie in de dnn module
#    net = cv.dnn.readNet("weights/yolov3-openimages.weights", "weights/yolov3-openimages.cfg")
    net = cv.dnn.readNet("Week_4/yolo_pretrained_model/yolov3.weights",
                                     "Week_4/yolo_pretrained_model/yolov3.cfg")

    # Laad de  namen van de objecten waarop ons model getraind is
    classes = []
    with open("Week_4/yolo_pretrained_model/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # hier linken we de namen aan de output layer neurons
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # stuur het geconfigureerde model retour
    return net, classes, colors, output_layers

#deze functie laad een plaatje (of frame van een video) in het geheugen
def load_image(img_path):
    # laad een image
    img = cv.imread(img_path)
    # schaal het plaatje voor efficientie
    #img = cv.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    return img, height, width, channels

#deze functie detecteert de objecten van een nieuw plaatje
def detect_objects(img, net, outputLayers):
    #blobFromImage zorgt voor het preprocessen van de data, waaronder
    #het schalen van de grijswaarden van 0 - 2555 naar 0 - 1 (scalefactor = 1/255)
    #het standaardiseren van de plaatjes naar 320 x 320 pixels
    #eventueel kun je nog mean_substraction doen (in dit geval niet nodig want onze pixels liggen al tussen de 0 en 1)
    #nog een boel andere magie
    blob = cv.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)

    #verbind ons voorbewerkt plaatje met het dnn
    net.setInput(blob)
    outputs = net.forward(outputLayers)

    return blob, outputs

#laten we de output omzetten in:
# het gevonden object (class_ids)
# boundingboxes  (boxes)
# een waarschijnlijkheidscore (confs)
def get_box_dimensions(outputs, height, width):
    boxes = []
    confs = []
    class_ids = []

    #loop over alle elementen (32x32 grid?) in output
    for output in outputs:

        #kijk per element welke labels erin zitten
        #zoek degene met de hoogste score
        for detect in output:
            scores = detect[5:]
#            print(scores)
            class_id = np.argmax(scores)
            conf = scores[class_id]

            center_x = int(detect[0] * width)
            center_y = int(detect[1] * height)
            w = int(detect[2] * width)
            h = int(detect[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confs.append(float(conf))
            class_ids.append(class_id)

    return boxes, confs, class_ids

#teken de voorspelling op het plaatje
def draw_labels(boxes, confs, colors, class_ids, classes, img):
    #Met de Non-Maximum Suppression (NMS)
    #halen we objecten op die minimaal een waarschijnlijkheidsscore van 30% hebben
    #en die voor minder dan 40% een overlap hebben met een boundingbox
    # van een object die als dezelfde klasse is geidentificeerd
    indexes = cv.dnn.NMSBoxes(boxes, confs, 0.3, 0.4)

    #van de boxen die overblijven: teken een rechthoek en zet er text bij
    font = cv.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]]) + "(" + str(round((confs[i])*100)) + "%)"
            color = colors[class_ids[i]]
            cv.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv.rectangle(img, (x,y-35), (x+w, y), color, cv.FILLED)
            cv.putText(img, label, (x, y - 5), font, 1, [255,255,255], 1)
    cv.imshow("Image", img)

