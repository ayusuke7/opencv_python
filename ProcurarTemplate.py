
import cv2
import numpy as np

def ProcurarTemplate(imagem, template):

    #Converte para escala de Cinza
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # cria delimitação do template
    result = cv2.matchTemplate(img_cinza, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    inf_rigth = (top_left[0] + 50, top_left[1] + 50)
    cv2.rectangle(imagem, top_left, inf_rigth, (0, 0, 255), 2)

    cv2.imshow('Imagem', imagem)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

#carrega a partir de arquivo
imagem = cv2.imread('resource\\pessoas.jpg')
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

#cria o template a ser encontrado
template = cv2.imread('resource\\cabeca.jpg', 0)

#Função
ProcurarTemplate(imagem, template)


