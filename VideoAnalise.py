import cv2
import numpy as np

cap = cv2.VideoCapture('resource\\video480.avi')
#cap = cv2.VideoCapture(0)

#aplica operador morphologico
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))
subtractor = cv2.createBackgroundSubtractorMOG2()

while True:

    ret, frame = cap.read()
    resultado = subtractor.apply(frame)
    #aplica operador morphologico
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('original', frame)
    cv2.imshow('resultado', resultado)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()