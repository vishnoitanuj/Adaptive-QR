import cv2
import numpy as np
from pyzbar import pyzbar
import json

class Decoder:

    def cropQR(self, image):
        barcodes = pyzbar.decode(image)
        qr_data_dict = dict()
        print(len(barcodes))
        for i, barcode in enumerate(barcodes):
            (x, y, w, h) = barcode.rect
            barcodeData = barcode.data.decode("utf-8")
            qr_data_dict.update(eval(barcodeData))
        return qr_data_dict
    
    def automatic_brightness_and_contrast(self, image, clip_hist_percent=15):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist_size = len(hist)

        accumulator = list()
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index-1]+float(hist[index]))
        
        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size -1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return (auto_result, alpha, beta)

    @staticmethod
    def base64_to_image(base64Image):
        imgdata = base64.b64decode(base64Image)
        image = cv2.imread(imgdata)
        return image

if __name__ == '__main__':
    image = cv2.imread('test.jpeg')
    decode = Decoder()
    im, _, _ = decode.automatic_brightness_and_contrast(image)
    images = decode.cropQR(im)
    print(images)