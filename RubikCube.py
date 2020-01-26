import cv2
import numpy as np
import DicionarioCor as dic


cube = [(255, 255, 255),(255, 255, 255),(255, 255, 255),
        (255, 0, 255),(255, 255, 0),(0, 255, 255),
        (255, 255, 255),(255, 255, 255),(255, 255, 255)]

pad = 55

kernel3 = np.ones((3, 3), np.uint8)
kernel5 = np.ones((5, 5), np.uint8)

cap = cv2.VideoCapture(0)


def drawing_cube(frame):

    for linha in range(3):
        for coluna in range(3):
            cv2.rectangle(frame, ((linha*50), 0),  ((linha*50)+50, (coluna*50)+50), cube[linha],   -1) 
            cv2.rectangle(frame, ((linha*50), 54), ((linha*50)+50, (coluna*50)+50), cube[linha+3], -1)
            cv2.rectangle(frame, ((linha*50), 100),((linha*50)+50, (coluna*50)+50), cube[linha+6], -1)

def drawing_points(frame):

    cor = dic.cores['verde']
    h, w = frame.shape[:2]  #lar = 640 x alt = 480

    points = [(w-(pad*3), h-(pad*3)), (w-(pad*2), h-(pad*3)), (w-(pad*1), h-(pad*3)),
              (w-(pad*3), h-(pad*2)), (w-(pad*2), h-(pad*2)), (w-(pad*1), h-(pad*2)),
              (w-(pad*3), h-(pad*1)), (w-(pad*2), h-(pad*1)), (w-(pad*1), h-(pad*1))]

    for i in range(9):
        cube[i] = get_color_pixel(frame, points[i][1], points[i][0])

    for p in points:
        cv2.circle(frame, p, 10, cor, -1)
    
def get_color_pixel(frame, posx, posy):
    (b, g, r) = frame[posx, posy]
    return (int(b), int(g), int(r))

def detect_color_hsv(frame):
     
    # Converte o espaco de cores RGB << HSV
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv, dic.min_amarelo, dic.max_amarelo)
    mask2 = cv2.inRange(hsv, dic.min_vermelho, dic.max_vermelho)
    
    target = cv2.bitwise_or(mask1, mask2)

    opem  = cv2.morphologyEx(target, cv2.MORPH_OPEN,  kernel3)
    close = cv2.morphologyEx(opem, cv2.MORPH_CLOSE, kernel3)
    erode = cv2.erode(close, kernel3, iterations=2)

    blur = cv2.medianBlur(erode, 7)
    #cv2.imshow('blur', blur)
    
    _, contours, _ = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

def detect_color_cnt(frame):
    
    #bilat = cv2.bilateralFilter(frame, 9, 75, 75)    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)    

    _, thresh	= cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh', thresh)

    #adaptive2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
    #cv2.imshow('adaptive2', adaptive2)

    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel3)
    erode = cv2.erode(close, kernel3, iterations=2)
    canny = cv2.Canny(erode, 100, 200)
    cv2.imshow('canny', canny)
    
    _, contours, _ = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = contours[0]
        perimetro = cv2.arcLength(c, True)
        if perimetro > 150:
            (x,	y, w, h) = cv2.boundingRect(c)

            roi = frame[y:y+alt, x:x+lar]
            detect_color_hsv(roi)
            
            cv2.rectangle(frame, (x,y), (x+w, y+h),	(0,	255, 0), 2)

    """
    for c in contours:
        perimetro = cv2.arcLength(c, True)
        #rect = cv2.minAreaRect(c)
        #box = cv2.boxPoints(rect)
        #box = np.intp(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        
        #(x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    """

def drawing_cnts(frame, contours):

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

if __name__== "__main__":

    while True:

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)    
        
        """ SEGMENTAÇÃO ROI """
        alt, lar = frame.shape[:2]
        roi = frame[int(alt/2):, int(lar/2):]
        
        #drawing_points(frame)    
        #drawing_cube(frame)

        detect_color_hsv(roi)
        #detect_color_cnt(roi)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xff == 27:
            break


    cap.release()
    cv2.destroyAllWindows()

