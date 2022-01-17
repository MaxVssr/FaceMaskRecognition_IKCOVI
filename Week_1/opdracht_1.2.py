import cv2 as cv

file ="Week_1\houses.jpg"
img = cv.imread(file)


if img is None:
    print("Fout bij het inlezen.")
else:
    print("Plaatje succesvol geladen")
    
    
cv.namedWindow('mijnWindow')
def muisEvent(event,x ,y ,flags ,param ):
    global img
    if event == cv.EVENT_LBUTTONDOWN:
        print('img[', y , ',' ,x,']: ', img[y,x])
        
cv.setMouseCallback('mijnWindow', muisEvent)

print(img.shape)

breedte = 4987
hoogte = 7477
ratio = breedte / hoogte
nieuweBreedte = 512
nieuweHoogte = nieuweBreedte * ratio
nieuwFormaat = (nieuweHoogte, nieuweBreedte)


cv.imshow('mijnWindow', img )
img = cv.resize(img, (hoogte,breedte), interpolation = cv.INTER_LINEAR)
img = cv.resize(img, (hoogte,breedte), interpolation = cv.INTER_CUBIC)
img = cv.resize(img, (hoogte,breedte), interpolation = cv.INTER_AREA)
cv.imwrite("houses_bewerkt2.jpg",img)


cv.imwrite('Week_1\HuisKlein.jpg', img, [cv.IMWRITE_PNG_COMPRESSION, 1])
cv.imwrite('Week_1\HuisKlein1.jpg', img, [cv.IMWRITE_JPEG2000_COMPRESSION_X1000, 1])
cv.imwrite('Week_1\HuisKlein2.jpg', img, [cv.IMWRITE_TIFF_COMPRESSION, 1])

while True :
    if cv.waitKey()==27:
        break
cv.destroyAllWindows()