#######################################################
#     Detecção de Placas atraves de retangulos        #
#                       by AY7                        #
#######################################################

import cv2
import numpy as np

def desenhaContornos(contornos, imagem):
    print("total de contornos ", len(contornos))
    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            #aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                cv2.drawContours(imagem, [c], -1, (0, 255, 0), 2)
            #else:
                #Desenha todos os demais contornos em vermelhos
                #cv2.drawContours(imagem, [c], -1, (0, 0, 255), 2)

    return imagem

#imagem original
img_original = cv2.imread('resource\carro4.jpg')
#cv2.imshow('ORIGINAL', img_original)

#escala de cinza
img_result = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#cv2.imshow('CINZA', img_result)

#binarização
ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)
cv2.imshow('THRESHOLDING', img_result)

#desfoque
img_result = cv2.GaussianBlur(img_result, (5, 5), 0)
#cv2.imshow('DESFOQUE', img_result)

img, contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

saida = desenhaContornos(contornos, img_original)
cv2.imshow('RESULTADO DES', saida)

recorte = []

cv2.waitKey(0)
cv2.destroyAllWindows()

