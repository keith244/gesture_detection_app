import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
"""
img = cv.imread(cv.samples.findFile("WIN_20260324_17_46_37_Pro.jpg"))
if img is None:
    sys.exit("Could not read the image")

cv.imshow("Display window", img)
k = cv.waitKey(0)
if k==ord("s"):
    cv.imwrite("WIN_PRO.jpg")"""
    
img = np.zeros((512, 512,3), np.uint8)
cv.line(img,(0,0),(511,511),(255,0,0),1)
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)




# rectangle 
cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
cv.circle(img,(447,63),63, (0,0,255),-1)
cv.ellipse(img,(256,256),(100,50),0,0,180,255,-1)

pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv.polylines(img,[pts],True,(0,255,255))


cv.imshow("image",img)
cv.waitKey(0)
cv.destroyAllWindows()

# image_path = 'WIN_20260324_17_46_37_Pro.jpg'

# img = cv2.imread(image_path)

# # convert to rgb and greyscale
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # display images
# plt.figure(figsize=(12,5))
# plt.subplot(1,2,1)
# plt.imshow(img_rgb)
# plt.title("Original Image (RGB)")
# plt.axis("off")

# plt.subplot(1,2,2)
# plt.imshow(img_gray, cmap='gray')
# plt.title("Grayscale image")
# plt.axis("off")

# plt.tight_layout()
# plt.show()