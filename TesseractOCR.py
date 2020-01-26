# --------------------------------------------#
#  Aplicação de Reconhecimento de Caracteres  #
#          Autor : Alexandre H                #
# --------------------------------------------#

from PIL import Image
import tkinter
import pytesseract
import cv2

class TesseractOCR():
    def __init__(self):
        pass

    def leituraImg(self, path_img):
        entrada = cv2.imread(path_img + ".jpg")

        # amplia a imagem da placa em 4
        img = cv2.resize(entrada, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("ENTRADA", img)

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
        texto = self.removerChars(saida)
        janela = tkinter.Tk()
        tkinter.Label(janela, text=texto, font=("Helvetica", 50)).pack()
        janela.mainloop()

        cv2.destroyAllWindows()

    def removerChars(self, text):
        str = "!@#%¨&*()_+:;><^^}{`?|~¬\/=,.'ºª»‘"
        for x in str:
            text = text.replace(x, '')
        return text

path = "C:/Tesseract-OCR/saidas/roi"
TesseractOCR().leituraImg(path)





