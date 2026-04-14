import cv2
import numpy as np

img = np.zeros((512, 512,3), np.uint8)
cv2.line(img,(0,0),(511,511),(255,0,0),10)
# cv2.rectangle(img,(50,150),(300,250),(0,255,0),3)
# cv2.circle(img, (256,256), 63, (0,0,255), -1)


cv2.imshow("Rectangle",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
