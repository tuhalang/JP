import cv2
import numpy as np
from cv2 import boundingRect, countNonZero, cvtColor, drawContours, findContours, getStructuringElement, imread, morphologyEx, pyrDown, rectangle, threshold

def detection(path_file):
    large = imread(path_file)
    # downsample and use it for processing
    rgb = pyrDown(large)
    # apply grayscale
    small = cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    # morphological gradient
    morph_kernel = getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = morphologyEx(small, cv2.MORPH_GRADIENT, morph_kernel)
    # binarize
    _, bw = threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    morph_kernel = getStructuringElement(cv2.MORPH_RECT, (9, 1))
    # connect horizontally oriented regions
    connected = morphologyEx(bw, cv2.MORPH_CLOSE, morph_kernel)
    mask = np.zeros(bw.shape, np.uint8)
    # find contours
    contours, hierarchy = findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    file = open(path_file.split(".")[0] + ".txt", "w")

    # filter contours
    for idx in range(0, len(hierarchy[0])):
        rect = x, y, rect_width, rect_height = boundingRect(contours[idx])
        # fill the contour
        mask = drawContours(mask, contours, idx, (255, 255, 2555), cv2.FILLED)
        # ratio of non-zero pixels in the filled region
        r = float(countNonZero(mask)) / (rect_width * rect_height)
        if r > 0.45 and rect_height > 50 and rect_width > 50:
            rgb = rectangle(rgb, (x, y+rect_height), (x+rect_width, y), (0,255,0),3)
            print((x, y, rect_width, rect_height))
            line = str(x) + "," + str(y) + "," + str(rect_width) + "," + str(rect_height) + "\n"
            file.writelines(line)

    file.close()
    cv2.imshow('rects', rgb)
    cv2.waitKey(0)

detection('/home/phamhung/Documents/Projects/JPHandwritingRecognition/text_detection/img.jpg')