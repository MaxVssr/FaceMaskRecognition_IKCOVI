import cv2 as cv
import numpy as np


file ='week_3/snelwegA2.png'; 

kleur_rood = [0,0,255]
kleur_groen = [0,255,0]
kleur_blauw = [255,0,0]

img = cv.imread(file)


if img is None:
    print("Fout bij het inlezen.")
else:
    print("Plaatje succesvol geladen")


cv.imshow("origineel", img)


gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

orb = cv.ORB_create()
kp = orb.detect(gray,None)

resultaat = cv.drawKeypoints(img, kp, None, color=kleur_groen,)
cv.imshow('resultaat',resultaat)



while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()
