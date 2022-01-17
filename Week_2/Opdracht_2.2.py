import cv2
import numpy as np
import matplotlib.pylab as plt

filename = "Week_2/ik.jpg"

image = cv2.imread(filename)
cv2.imshow("origineel",image)

num_down = 2 
num_bilateral = 7
w, h, _ = image.shape

img_color = np.copy(image)
for _ in range(num_down):
    img_color = cv2.pyrDown(img_color)
    

for _ in range(num_bilateral):
    img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=0.1, sigmaSpace=0.01)

for _ in range(num_down):
    img_color = cv2.pyrUp(img_color)

img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
img_blur = cv2.medianBlur(img_gray, 7)

img_edge = cv2.adaptiveThreshold((255*img_blur).astype(np.uint8), \
255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, \
blockSize=9, C=2)

img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
img_cartoon = cv2.bitwise_and(img_color, img_color, mask = img_edge)


fig = plt.figure(figsize=(20,10))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05) 
plt.subplot(121)
plt.imshow(image)
plt.axis('off')
plt.title('Original Image', size=20)
plt.subplot(122)
plt.imshow(img_cartoon)
plt.axis('off')
plt.title('Cartoonized Image', size=20)
plt.show()


# # importing libraries
# import cv2
# import numpy as np

# # reading image 
# img = cv2.imread("Week_2/ik.jpg")

# # Edges
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.medianBlur(gray, 9)
# edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
#                                         cv2.THRESH_BINARY, 9, 9)

# # Cartoonization
# color = cv2.bilateralFilter(img, 9, 250, 250)
# cartoon = cv2.bitwise_and(color, color, mask=edges)


# cv2.imshow("Image", img)
# cv2.imshow("edges", edges)
# cv2.imshow("Cartoon", cartoon)
# cv2.waitKey(0)
# cv2.destroyAllWindows()