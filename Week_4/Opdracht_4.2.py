import cv2 as cv
import numpy as np

boxes = []
confs = []
class_ids = []
kleur_wit = [255, 255, 255]
font = cv.FONT_HERSHEY_PLAIN

plaatje = "Week_4/sleutelstad_2015_08_fietsfout.jpg"
img = cv.imread(plaatje)

img = cv.resize(img, None, fx = 0.6, fy = 0.6)
hoogte, breedte, kleuren = img.shape

#................................................................

net = cv.dnn.readNet("Week_4/yolo_pretrained_model/yolov3.weights", "Week_4/yolo_pretrained_model/yolov3.cfg")

layers_names = net.getLayerNames()
output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]

classes = []
with open("Week_4/yolo_pretrained_model/coco.names", "r") as f:
    classes = [line.strip()
                for line in f.readlines()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

blob = cv.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
net.setInput(blob)
outputs = net.forward(output_layers)

for output in outputs:
    for detect in output:
        scores = detect[5:]
        class_id = np.argmax(scores)
        conf = scores[class_id]

        center_x = int(detect[0] * hoogte)
        center_y = int(detect[1] * hoogte)
        w = int(detect[2] * breedte)
        h = int(detect[3] * hoogte)
        x = int(center_x - w / 2)
        y = int(center_y - h / 2)

        boxes.append([x, y, w, h])
        confs.append(float(conf))
        class_ids.append(class_id)

indexes = cv.dnn.NMSBoxes(boxes, confs, 0.1, 0.4)

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
            cv.rectangle(tmp, (x, y -35), (x + w, y), color, cv.FILLED)
            cv.putText(tmp, label, (x, y -5), font, 1, kleur_wit, 1)
    cv.imshow('window', tmp)
    

cv.namedWindow('window')
cv.createTrackbar('confidence', 'window', 0, 100, bbox_met_score_hoger_dan_trackbar)
cv.setTrackbarPos('confidence', 'window', 50)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break