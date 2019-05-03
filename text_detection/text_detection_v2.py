import cv2

def cut_table(url):
    img = cv2.imread(url, 0)
    blur = cv2.GaussianBlur(img,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    horizal = thresh
    vertical = thresh

    scale_height = 20
    scale_long = 15

    long = int(img.shape[1]/scale_long)
    height = int(img.shape[0]/scale_height)

    horizalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (long, 1))
    horizal = cv2.erode(horizal, horizalStructure, (-1, -1))
    horizal = cv2.dilate(horizal, horizalStructure, (-1, -1))

    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height))
    vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
    vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

    mask = vertical + horizal

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    table = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 10 and w > 10:
            square = cv2.contourArea(cnt)
            table.append((square,x,y,w,h))

    table.sort(reverse=True)
    for i in range(len(table)):
        sub_img = img[table[i][2]:table[i][2]+table[i][4], table[i][1]:table[i][1]+table[i][3]]
        cv2.imwrite('sub_' + str(i) + '_' + url, sub_img)


if __name__ == "__main__":
    url = 'aaaa.jpg'
    cut_table(url)