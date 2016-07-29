import cv2
import numpy as np

img = cv2.imread('lightning.jpg', 0)
blur =  cv2.GaussianBlur(img,(11,11),0)
cv2.imshow('img',blur)
cv2.waitKey()
ret, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
cv2.imshow('img',thresh)
cv2.waitKey()
cv2.imwrite('thresh.jpg',thresh)
im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
img_count = 0
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    roi = img[y:y + h, x:x + w]
    cv2.imwrite("roi{}.png".format(img_count), roi)
    img_count+=1
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
cv2.imwrite('done.jpg',img)
#cv2.imshow('img',img)
#cv2.waitKey()