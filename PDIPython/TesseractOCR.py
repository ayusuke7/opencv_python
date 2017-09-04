# ------------------------------------------#
#  Aplication Reconhecimento de Caracteres  #
#          Autor : Alexandre H              #
# ------------------------------------------#

from PIL import Image
import pytesseract
import numpy as np
import cv2

def lerImagemOCR(path_imagem, img):
    cv2.imwrite(path_imagem, img)
    imagem = Image.open(path_imagem)
    saida = pytesseract.image_to_string(imagem, lang='eng')
    print(saida)
    return saida

path = "C:/Tesseract-OCR/ocr2"

img = cv2.imread(path+".jpg")

# ConvertE para escala de cinza
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Imagem Cinza", img)

#gray = np.float32(img)
#dst = cv2.cornerHarris(gray, 2, 3, 0.04)
#img = cv2.dilate(dst, None)
#cv2.imshow("Imagem Dilatada", img)

#Binariza imagem
ret, img = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)
cv2.imshow("Imagem Binaria", img)

#Desfoque na Imagem
img = cv2.GaussianBlur(img, (5, 5), 0)
cv2.imshow("Imagem Desfocada", img)

lerImagemOCR(path+"-saida.jpg", img)

cv2.waitKey(0)
cv2.destroyAllWindows()



