############################################################
#     Reconhecimento de Placas atraves de contornos        #
#                            by AY7                        #
############################################################

from PIL import Image
import numpy as np
import tkinter
import pytesseract
import cv2

def desenhaContornos(contornos, imagem):

    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
           #aproxima os contornos da forma correspondente
           approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
           #verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
           if len(approx) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x + alt, y + lar), (255, 0, 0), 2)
                #cv2.drawContours(imagem, [c], -1, (0, 255, 0), 1)
                roi = imagem[(y+15):y + lar, x:x + alt]
                #amplia a imagem 4x
                cv2.imwrite("C:/Tesseract-OCR/saidas/roi-img.jpg", roi)

    return imagem

def reconhecimentoOCR(path_img):

    entrada = cv2.imread(path_img + ".jpg")

    # amplia a imagem da placa em 4
    img = cv2.resize(entrada, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Escala Cinza", img)

    # Binariza imagem
    ret, img = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow("Limiar", img)

    # Desfoque na Imagem
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow("Desfoque", img)

    cv2.imwrite(path_img + "-ocr.jpg", img)
    imagem = Image.open(path_img + "-ocr.jpg")
    saida = pytesseract.image_to_string(imagem, lang='eng')
    print(saida)
    texto = removerChars(saida)
    janela = tkinter.Tk()
    tkinter.Label(janela, text=texto, font=("Helvetica", 50)).pack()
    janela.mainloop()

    # cv2.waitKey(0)
    cv2.destroyAllWindows()

def removerChars(text):
    str = "!@#%¨&*()_+:;><^^}{`?|~¬\/=,.'ºª»‘"
    for x in str:
        text = text.replace(x, '')
    return text

#imagem original
img_original = cv2.imread('resource\carro4.jpg')

#escala de cinza
img_result = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

#binarização
ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)

#desfoque
img_result = cv2.GaussianBlur(img_result, (5, 5), 0)

img, contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

saida = desenhaContornos(contornos, img_original)

#limite horizontal 1
cv2.line(saida,(0, 220), (600, 220), (0, 0, 255), 2)
#limite horizontal 2
cv2.line(saida,(0, 350), (600, 350), (0, 0, 255), 2)

#limite vertical 1
cv2.line(saida,(200, 0), (200, 480), (0, 0, 255), 2)
#limite vertical 2
cv2.line(saida,(400, 0), (400, 480), (0, 0, 255), 2)

cv2.imshow('SAIDA', saida)

reconhecimentoOCR("C:/Tesseract-OCR/saidas/roi-img")

