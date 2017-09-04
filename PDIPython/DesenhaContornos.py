import cv2
import numpy as np

#imagem original
img_binaria = cv2.imread('resource\\formas_binario.jpg')

#imagem desfocada
img_desfocada = cv2.GaussianBlur(img_binaria, (5, 5), 0)

#imagem escala de cinza
img_binaria_gray = cv2.cvtColor(img_desfocada, cv2.COLOR_BGR2GRAY)

padrao = cv2.RETR_TREE
#padrao = cv2.RETR_EXTERNAL

img, cont, hier = cv2.findContours(img_binaria_gray, padrao, cv2.CHAIN_APPROX_NONE)

for c in cont:
    perimetro = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * perimetro, True)
    cv2.drawContours(img_binaria, [c], -1, (0,0,255), 2)

    #dimensoes das formas
    posX, posY, alt, lar = cv2.boundingRect(c)
    print(posX, posY, alt, lar)

cv2.imshow('RESULTADO GRAY', img_binaria_gray)
cv2.imshow('RESULTADO', img_binaria)

cv2.waitKey(0)
cv2.destroyAllWindows()