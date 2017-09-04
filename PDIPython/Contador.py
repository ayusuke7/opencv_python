import cv2
import numpy as np

#imagem original
img_original = cv2.imread('resource\contador4x8.jpeg')
cv2.imshow('IMG ORIGINAL', img_original)

#escala de cinza
img_saida = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#cv2.imshow('IMG CINZA', img_saida)

#binariza a imagem
ret, img_saida = cv2.threshold(img_saida, 70, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('IMG BINARIA', img_saida)

#img_saida = cv2.adaptiveThreshold(img_saida, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#desfoca imagem
#img_saida = cv2.GaussianBlur(img_saida, (5, 5), 1)
#cv2.imshow('DESFOQUE', img_desfocada)

padrao = cv2.RETR_TREE
#padrao = cv2.RETR_EXTERNAL
img, contornos, hier = cv2.findContours(img_saida, padrao, cv2.CHAIN_APPROX_NONE)

for c in contornos:
   cv2.drawContours(img_original, [c], -1, (0, 0, 255), 1)

cv2.imshow('RESULTADO', img_original)
cv2.waitKey(0)
cv2.destroyAllWindows()