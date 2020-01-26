import cv2
import numpy as np

kernel3 = np.ones((3, 3), np.uint8)
kernel5 = np.ones((5, 5), np.uint8)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
line = cv2.LINE_AA

def Rotate(img, angulo=90):
    rows, cols = img.shape[:2]
    matriz = cv2.getRotationMatrix2D((cols/2, rows/2), angulo, 1)
    result = cv2.warpAffine(img, matriz, (cols, rows))
    return result

def Tranformations(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)

    ret, thresh = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV)
    
    morph = cv2.dilate(blur, kernel3, iterations = 2)
    morph = cv2.erode(morph, kernel3, iterations = 2)

    canny = cv2.Canny(blur, 100, 200)
    cv2.imshow('canny', canny)

    sobelx = cv2.Sobel(morph, cv2.CV_8U, 1, 0, ksize = 3)
    cv2.imshow('sobelx', sobelx)
    
    sobely = cv2.Sobel(morph, cv2.CV_8U, 0, 1, ksize = 3)
    cv2.imshow('sobely', sobely)

if __name__ == "__main__":

    cap = cv2.VideoCapture('resource/video-contador.mp4')

    while True:

        ret, img = cap.read()

        if not ret:
            break

        alt, lar = img.shape[:2]
        roi = img[:, lar-30:]

        size = 1.5
        zoom = cv2.resize(roi, None, fx=size, fy=size, interpolation=cv2.INTER_CUBIC)
        
        Tranformations(zoom)

        cv2.line(img, (lar-30, 0), (lar-30, alt), (0, 255, 0), 2)  
        
        cv2.imshow("video",	img)
        cv2.imshow('zoom', zoom)        
        
        if cv2.waitKey(33) == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()