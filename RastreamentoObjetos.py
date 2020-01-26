import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    #converte a escala de cor RGB para HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define o intervalo da cor azul no HSV
    min_azul = np.array([110, 50, 50])
    max_azul = np.array([130, 255, 255])

    # Liminarizar a imagem HSV para obter apenas cores azuis
    mascara = cv2.inRange(img_hsv, min_azul, max_azul)

    # Mascara Bitwise-AND e a original image
    result = cv2.bitwise_and(frame, frame, mask=mascara)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mascara)
    cv2.imshow('res', result)

    if cv2.waitKey(1) == ord('q'):
       break

cv2.destroyAllWindows()


