import cv2
import numpy as np

kernel3 = np.ones((3, 3), np.uint8)
kernel5 = np.ones((5, 5), np.uint8)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
line = cv2.LINE_AA

cont = 0

def RoiBox(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)
    _, thresh = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY_INV)
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    aux = img.copy()

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(aux, [box], 0, (0, 0, 255), 2)
        (x, y, w, h) = cv2.boundingRect(c)
        roi = img[y:y+h, x:x+w]
    
    cv2.imshow('rect roi', aux)
    return roi

def FindLines(img):

    alt, lar = img.shape[:2]
    roi = img[:, int(lar/2)-10:int(lar/2)]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)

    _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('thresh', thresh)
    
    sobel = cv2.Sobel(thresh, cv2.CV_8U, 0, 1, ksize=5)
    #cv2.imshow('sobel', sobel)   

    im, cnts, hier = cv2.findContours(sobel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    draw = DrawContorns(roi, cnts)

    img[:, int(lar/2)-10:int(lar/2)] = draw
    cv2.putText(img, 'Cont: '+str(cont), (20, 30), font, 1, (255, 255, 255), 1, line)
    cv2.imshow('result', img)

def DrawHoughLines(img, lines):

    if lines is not None:
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
    
                cv2.line(img,(x1,y1),(x2,y2),(0, 255, 0), 1)
    
    cv2.imshow('DrawLines', img)

def DrawContorns(img, contours):

    global cont

    for c in contours:
        color = (0, 0, 255) 
        if cont % 2 == 0: color = (0, 255, 0) 
        cv2.drawContours(img, [c], 0, color, 2)
        cont += 1

    print(cont)
    return img

if __name__ == "__main__":

    paths = ['contador3x6.jpeg', 'contador4x8.jpeg', 'img2.jpg']
    img = cv2.imread('resource/'+paths[1])

    area = RoiBox(img)
    FindLines(area)

    cv2.waitKey(0)
    cv2.destroyAllWindows()