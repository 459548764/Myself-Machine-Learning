
import cv2
import numpy as np

imgHeight = 600
imgWidth = 400

img = cv2.imread('tokyo.jpg',cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(imgHeight,imgWidth))

threshold = 90
while(1):
    low_mean = 0
    low_cnt = 0
    high_mean = 0
    high_cnt = 0
    for i in range(imgWidth):
        for j in range(imgHeight):
            if(img[i][j] <= threshold):
                low_cnt += 1
                low_mean += img[i][j]
            else:
                high_cnt += 1
                high_mean += img[i][j]
    avr = (low_mean/low_cnt + high_mean/high_cnt)/2
    if(np.abs(avr - threshold) <= 0.5):
        break
    else:
        print(threshold)
        threshold = avr


