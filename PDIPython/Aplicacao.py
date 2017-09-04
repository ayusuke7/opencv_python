import cv2
import numpy as np

imagemOriginal = cv2.imread('resource\contador3x6.jpeg')
#imagemDesfocada = cv2.GaussianBlur(imagem, (5, 5), 0)
imagemCinza = cv2.cvtColor(imagemOriginal, cv2.COLOR_BGR2GRAY)

#ret,imagemBinaria = cv2.threshold(imagemCinza,70,255,cv2.THRESH_BINARY)
#ret,imagemBinaria = cv2.threshold(imagemCinza,70,255,cv2.THRESH_BINARY_INV)

padrao = cv2.RETR_TREE
#padrao = cv2.RETR_EXTERNAL

img, contornos, hierarquia = cv2.findContours(imagemCinza, padrao, cv2.CHAIN_APPROX_SIMPLE)

for c in contornos:
    cv2.drawContours(imagemOriginal, [c], -1, (0,0,255), 3)

cv2.imshow("CONTORNO", imagemOriginal)
#cv2.imshow("ORIGINAL", imagemBinaria)
#cv2.imshow("IMAGEM 2", imagemBin2)

cv2.waitKey(0)
cv2.destroyAllWindows()