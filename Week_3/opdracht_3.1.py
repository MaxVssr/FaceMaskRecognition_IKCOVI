import cv2 as cv
import numpy as np

file = 'week_3/snelwegA2.png'

kleur_rood = [0, 0, 255]
kleur_groen = [0, 255, 0]
kleur_blauw = [255, 0, 0]

img = cv.imread(file)

if img is None:
    print("Fout bij het inlezen.")
else:
    print("Plaatje succesvol geladen")


cv.imshow("origineel", img)


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 100, 400, apertureSize = 3)
cv.imshow("edges", edges)

#lijnen = cv.HoughLines(edges, 1, np.pi/180, 150)
lijnenRechts = cv.HoughLines(edges, 1, np.pi/180, 150, min_theta=2/3*np.pi, max_theta=5/6*np.pi)
lijnenLinks = cv.HoughLines(edges, 1, np.pi/180, 300, min_theta=1/3*np.pi, max_theta=2/5*np.pi)
lijnen = np.concatenate((lijnenRechts, lijnenLinks), axis= 0)

circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=20)
circles = np.uint16(np.around(circles))[0, :]
for centerx, centery, radius in circles:
    cv.circle(img, (centerx, centery), radius, kleur_groen, 2)
    cv.circle(img, (centerx, centery), 2, kleur_blauw, 3)




nlijnen, punt, nDimenties = lijnen.shape
for i in range (nlijnen):
    rho, theta = lijnen[i][0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv.line(img, (x1,y1), (x2, y2), kleur_rood, 2)

cv.imshow('resultaat', img)
cv.imshow('snelweg_output.jpg', img)


while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()