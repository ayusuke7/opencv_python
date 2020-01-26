#######################################################
#     Detecção de Placas atraves de contornos  HD     #
#                       by AY7                        #
#######################################################

from PIL import Image
import numpy as np
import tkinter
import pytesseract
import cv2

def findPlace(contornos, imagem):#

    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 200 and perimetro < 600:
           #aproxima os contornos da forma correspondente
           approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
           #verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
           if len(approx) == 4:
             #Contorna a placa atraves dos contornos encontrados
             #cv2.drawContours(imagem, [c], -1, (0, 255, 0), 2)
             (x, y, lar, alt) = cv2.boundingRect(c)
             cv2.rectangle(imagem, (x, y), (x + lar, y + alt), (0, 255, 0), 2)
             #segmenta a placa da imagem
             roi = imagem[(y+15):y+alt, x:x+lar]
             #salva a imagem segmentada em "C:/Tesseract-OCR/saidas/"
             cv2.imwrite("C:/Tesseract-OCR/saidas/roi.jpg", roi)
                
    return imagem

def reconhecimentoOCR(path_img):

    #Ler a entrada da imagem e salva na variavel entrada
    entrada = cv2.imread(path_img + ".jpg")
    # cv2.imshow("ENTRADA", img)

    # aumenta a resoluca da imagem da placa em 4x
    img = cv2.resize(entrada, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Escala Cinza", img)

    # Binariza a imagem (preto e branco)
    ret, img = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow("Limiar", img)

    # Aplica um desfoque na Imagem
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow("Desfoque", img)
    
    # Grava o resultado no endereco path+/ocr.jpg
    cv2.imwrite(path_img + "-ocr.jpg", img)
    
    # Abre a imagem gravada para ser feita o reconhecimento OCR
    # e salva o resultado na variavel saida
    imagem = Image.open(path_img + "-ocr.jpg")
    saida = pytesseract.image_to_string(imagem, lang='eng')

    # Realiza um filtro nos caracteres obtidos 
    # eliminando possiveis ruidos reconhecidos
    if len(saida) > 0:
        print(saida)
        texto = removerChars(saida)
    else:
        texto = "Reconhecimento Falho"

    janela = tkinter.Tk()
    tkinter.Label(janela, text=texto, font=("Helvetica", 50)).pack()
    janela.mainloop()

def removerChars(text):
    str = "!@#%¨&*()_+:;><^^}{`?|~¬\/=,.'ºª»‘"
    for x in str:
        text = text.replace(x, '')
    return text

#Captura ou Video
video = cv2.VideoCapture('resource\\video1-720p.mkv')

while(video.isOpened()):

    ret, frame = video.read()

    if(ret == False):
        break

    #area de localização
    area = frame[500: , 300:800]

    # escala de cinza
    img_result = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

    # limiarização
    ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)

    # desfoque
    img_result = cv2.GaussianBlur(img_result, (5, 5), 0)

    # lista os contornos
    img, contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # limite horizontal
    cv2.line(frame, (0, 500), (1280, 500), (0, 0, 255), 1)
    # limite vertical 1
    cv2.line(frame, (300, 0), (300, 720), (0, 0, 255), 1)
    # limite vertical 2
    cv2.line(frame, (800, 0), (800, 720), (0, 0, 255), 1)

    cv2.imshow('FRAME', frame)

    findPlace(contornos, area)

    cv2.imshow('RES', area)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video.release()
reconhecimentoOCR("C:/Tesseract-OCR/saidas/roi")
cv2.destroyAllWindows()
