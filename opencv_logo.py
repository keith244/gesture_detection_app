import cv2 as cv
import numpy as np

# create black image bg
# img = np.zeros((512,512,3),np.uint8)
img = np.full((600,500,3),255, dtype=np.uint8)

# drawig triangle
"center it"
cx , cy = 256,256

"define its points"
size = 100 
pts = np.array([
    [cx, cy - size],
    [cx - size, cy +  size],
    [cx + size, cy +  size],
], np.int32)

pts = pts.reshape((-1,1,2))

cv.polylines(img,[pts],isClosed=True, color=(0,255,255), thickness=3)

# create circle
cv.circle(img,(477,63),63,(0,0,255), -1)

cv.line(img, (0, 0), (250, 0), 0, 10)
# Vertical line from top-left
cv.line(img, (0, 0), (0, 300), 0, 10)

cv.imshow("Centerd triangle", img)
cv.waitKey(0)
cv.destroyAllWindows()
