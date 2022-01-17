import cv2 as cv
import numpy as np
import argparse
import time

#implementatie overgenomen van
# https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

from yolo_algoritme_functies import *

def image_detect(img_path):

    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    draw_labels(boxes, confs, colors, class_ids, classes, image)

    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def webcam_detect(cap):
    model, classes, colors, output_layers = load_yolo()

    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def start_video(video_path):
    model, classes, colors, output_layers = load_yolo()
    cap = cv.VideoCapture(video_path)

    # lees eerste frame in om de defaults te verkrijgen
    ret, frame = cap.read()
    if not ret:
        print("Kon video niet inlezen")
        return

    framenr = 0
    height, width, layers = frame.shape

    while True:
        #do acties op het frame
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        #tijd voor het volgende frame
        ret, frame = cap.read()
        if not ret:
            print("klaar met de film na " +str(framenr)+  " frames")
            break
        framenr +=1

    cap.release()


plaatje = "Week_4/sleutelstad_2015_08_fietsfout.jpg"
image_detect(plaatje)

# video ="Week_4/pedestrians.mp4"
# start_video(video)

#detecteert objecten voor jouw webcam
# cap = cv.VideoCapture(0)
# webcam_detect(cap)
# cap.release()
