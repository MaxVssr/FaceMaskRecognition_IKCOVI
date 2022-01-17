# import cv2 as cv
# import numpy as np

# #initialisaties voor later
# boxes = []
# confs = []
# class_ids = []
# kleur_wit = [255, 255, 255]
# font = cv.FONT_HERSHEY_PLAIN

# #lees het plaatje in:
# plaatje = "D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_4/sleutelstad_2015_08_fietsfout.jpg"
# img = cv.imread(plaatje)

# #we maken het wat kleiner voor de snelheid
# img = cv.resize(img, None, fx=0.6, fy=0.6)
# hoogte, breedte, kleuren = img.shape

# #hier komt al onze nieuwe code
# net = cv.dnn.readNet("D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_4/yolo_pretrained_model/yolov3.weights", "D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_4/yolo_pretrained_model/yolov3.cfg")

# layers_names = net.getLayerNames()
# output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]


# classes = []
# with open ("D:/Oud Bureaublad/School/Hogeschool Leiden/Jaar_3/IKCOVI/Week_4/yolo_pretrained_model/coco.names", "r") as f:
#     classes = [line.strip()
#                 for line in f.readlines()]
# colors = np.random.uniform(0, 255, size = (len(classes), 3))

# blob = cv.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
# net.setInput(blob)
# outputs = net.forward(output_layers)

# # loop over alle elementen in de image pyramide van outputs
# for output in outputs:
#     # lees voor de image pyramide output de boundingbox +
#     # voorspelling van elke klasse in
#     for detect in output:
#         scores = detect[5:]
#         class_id = np.argmax(scores)
#         conf = scores[class_id]
#         #bereken de boundingbox:
#         center_x = int(detect[0] * breedte)
#         center_y = int(detect[1] * hoogte)
#         w = int(detect[2] * breedte)
#         h = int(detect[3] * hoogte)
#         x = int(center_x - w / 2)
#         y = int(center_y - h / 2)
#         # sla alles op in een lijsten zodat ze
#         # gemakkelijker in en uit te lezen zijn
#         boxes.append([x, y, w, h])
#         confs.append(float(conf))
#         class_ids.append(class_id)


# def bbox_met_score_hoger_dan_trackbar(waarschijnlijkheid):
#     # goede coding practise: benoem hier welke globale variabelen
#     # je gebruikt
#     global img
#     global boxes
#     global confs
#     global colors
#     global class_ids
#     global kleur_wit
#     global font
#     #eventjes een kopie zodat we niet over hetzelfde plaatje heen tekenen
#     tmp = img.copy()
    
#     # wat is de drempelwaarde die we willen laten zien
#     # even omrekenen van 0 - 100 naar 0 - 1 scores
#     conf_drempel = waarschijnlijkheid / 100
#     #hier lopen we over alle boxes heen
#     for i in range(len(boxes)):
#     # we tekenen degene met een waarschijnlijkheidsscore groter dan de
#     # ingestelde drempelwaarde van de trackbar
#         if (conf_drempel < confs[i]):
#             x, y, w, h = boxes[i]
#             label = str(classes[class_ids[i]]) + \
#                     "(" + str(round((confs[i]) * 100)) + "%)"
#             color = colors[class_ids[i]]
#             cv.rectangle(tmp, (x, y), (x + w, y + h), color, 2)
#             cv.rectangle(tmp, (x, y - 35), (x + w, y), color, cv.FILLED)
#             cv.putText(tmp, label, (x, y - 5), font, 1, kleur_wit, 1)
#     cv.createTrackbar('confidence', 'window', 0, 100, bbox_met_score_hoger_dan_trackbar)
#     cv.setTrackbarPos('confidence', 'window', 50)






# #laat het Plaatje zien
# cv.namedWindow('window')
# cv.imshow('window', img)
# while True:
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break


import cv2 as cv
import numpy as np

boxes = []
confs = []
class_ids = []
kleur_wit = [255, 255, 255]
font = cv.FONT_HERSHEY_PLAIN

plaatje = "Week_4/sleutelstad_2015_08_fietsfout.jpg"
img = cv.imread(plaatje)
img = cv.resize(img, None, fx=0.6, fy=0.6)
hoogte, breedte, kleuren = img.shape


net = cv.dnn.readNet("Week_4/yolo_pretrained_model/yolov3.weights", "Week_4/yolo_pretrained_model/yolov3.cfg")

layers_names = net.getLayerNames()
output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]

classes = []
with open("Week_4/yolo_pretrained_model/coco.names", "r") as f:
    classes = [line.strip() 
    for line in f.readlines()]
colors = np.random.uniform(0, 255, size = (len(classes), 3))

blob = cv.dnn.blobFromImage(img, scalefactor = 0.00392, size = (320,320), mean = (0,0,0), swapRB = True, crop = False)
net.setInput(blob)
outputs = net.forward(output_layers)


for output in outputs:
    for detect in output:
        scores = detect[5:]
        class_id = np.argmax(scores)
        conf = scores[class_id]
        
        center_x = int(detect[0] * breedte)
        center_y = int(detect[1] * hoogte)
        w = int(detect[2] * breedte)
        h = int(detect[3] * hoogte)
        x = int(center_x -w / 2)
        y = int(center_y -h / 2)
        
        boxes.append([x, y, w, h])
        confs.append(float(conf))
        class_ids.append(class_id)



def bbox_met_score_hoger_dan_trackbar(waarschijnlijkheid):
    global img
    global boxes
    global confs
    global colors
    global class_ids
    global kleur_wit
    global font

    tmp = img.copy()
    
    conf_drempel = waarschijnlijkheid / 100

    for i in range(len(boxes)):
        if (conf_drempel < confs[i]):
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]]) + \
                "(" + str(round((confs[i]) * 100)) + "%)"
            color = colors[class_ids[i]]
            cv.rectangle(tmp, (x, y), (x + w, y + h), color, 2)
            cv.rectangle(tmp, (x, y - 35), (x + w, y), color, cv.FILLED)
            cv.putText(tmp, label, (x, y - 5), font, 1, kleur_wit, 1)
    cv.imshow('window', tmp)
    

cv.namedWindow('window')
cv.createTrackbar('confidence', 'window', 0, 100, bbox_met_score_hoger_dan_trackbar)
cv.setTrackbarPos('confidence', 'window', 50)
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break