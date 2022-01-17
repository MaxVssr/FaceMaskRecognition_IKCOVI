import cv2 as cv






#Leest het plaatje van file
#LET OP: geef het juiste pad op naar het plaatje
file ="Week_1\openCVlogo.png"
img = cv.imread(file)
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

#test of het plaatje goed is ingelezen
if img is None:
    print("Fout bij het inlezen.")
else:
    print("Plaatje succesvol geladen")
    
    
cv.namedWindow('mijnWindow')

# breedte = 7477
# hoogte = 4987

# ratio = breedte / hoogte
# nieuweBreedte = 512
# nieuweHoogte = int(nieuweBreedte * ratio)
# nieuwFormaat = (nieuweHoogte, nieuweBreedte)
# img = cv.resize(img, nieuwFormaat)


def muisEvent(event,x ,y ,flags ,param ):
    global img
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, img[y,x],5,  (255,255,255), 5 )
        print('img[', y , ',' ,x,']: ', img[y,x])
        
cv.setMouseCallback('mijnWindow', muisEvent)


# print(img.size)
cv.imshow('mijnWindow', img )
cv.imwrite('Week_1\openCVlogo.jpg', img)
# cv.waitKey(27)
while True :
    if cv.waitKey()==27:
        break
cv.destroyAllWindows()



# # img = cv.resize(img, (hoogte, breedte))
# # cv.imwrite("houses_bewerkt.jpg",img)


# cv.imwrite('HuisKlein.jpg', img, [cv.IMWRITE_JPEG2000_COMPRESSION_X1000, 512])
# def muisEvent(event,x ,y ,flags ,param ):
#     global img
#     if event == cv.EVENT_LBUTTONDOWN:
#         print('img[', y , ',' ,x,']: ', img[y,x])
# #print alleen maar iets als er de linkermuisknop
# #ingedrukt is:

# cv.setMouseCallback( 'mijnWindow' ,muisEvent )
# while True :
#     if cv.waitKey()==27:
#         break
# cv.destroyAllWindows()





import cv2 as cv

file ="Week_1\openCVlogo.png"
img = cv.imread(file)
img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # 3. De verrassing waar je voor komt te staan is dat de kleuren 
                                         #    van plaats wisselen maar openCV nog steeds BGR lees ipv RGB en je 
                                         #    hierdoor dus hele andere kleuren krijgt.

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
cv.imshow('mijnWindow', img )
cv.imwrite('Week_1\openCVlogo.jpg', img)

while True :
    if cv.waitKey()==27:
        break
cv.destroyAllWindows()
