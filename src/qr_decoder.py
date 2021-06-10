#qr code detection
import cv2
import numpy as np
from pyzbar.pyzbar import decode

#qr decoder function
def decoder(image):
    grayscale_img = cv2.cvtColor(image,0)
    barcode = decode(grayscale_img)
    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        Dict = eval(barcodeData)
        print(Dict)
        print("Type:", type(Dict))
        string = "Data " + str(barcodeData)
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 1)

# inverse image and save
frame = cv2.imread('test.jpg')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
qr = cv2.bitwise_not(gray)
cv2.imwrite('4qr.png', qr)
image = cv2.imread('4qr.png')
original = image.copy()

#blur and threshold
blur = cv2.GaussianBlur(gray, (25,25), 0)
cv2.imshow('blur', blur)
th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
cv2.imshow('th', th)

# Morphological opening and closing
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations = 2)
cv2.imshow('opening', opening)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 5)
cv2.imshow('close', close)

# Find contours and filter for QR code
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    #creating detection box
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * perimeter, True)
    x,y,w,h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        qr = original[y:y+h, x:x+w]
        decoder(qr)

cv2.imshow('image', image)
cv2.imshow('qr', qr)
cv2.waitKey()