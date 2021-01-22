import cv2
import pytesseract
import numpy as np
import requests
import base64
import json


def showText(text="text", alt=400, lar=600):

    shape = [alt, lar, 3]  # alt lar canais
    lineType = cv2.LINE_AA
    font = cv2.FONT_HERSHEY_PLAIN
    font_color = [0, 0, 0]

    blank_image = np.ones(shape=shape, dtype=np.uint8) * 255

    if type(text) is list:
        for i, t in enumerate(text):
            cv2.putText(blank_image, t, (10, 50 + (i * 50)), font,
                        3, font_color, lineType=lineType)
    else:
        cv2.putText(blank_image, text, (20, 50), font,
                    3, font_color, lineType=lineType)

    cv2.imshow("text", blank_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def encontrarRoiPlaca(source):
    img = cv2.imread(source)
    # cv2.imshow("img", img)

    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("cinza", img)

    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    # cv2.imshow("binary", img)

    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    # cv2.imshow("defoque", desfoque)

    contornos, hierarquia = cv2.findContours(
        desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contornos, -1, (0, 255, 0), 1)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
                roi = img[y+12:(y + lar)-5, x+5:(x + alt)-10]
                cv2.imwrite('output/roi.png', roi)

    cv2.imshow("contornos", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preProcessamentoRoi():
    img_roi = cv2.imread("output/roi.png")

    if img_roi is None:
        return

    img_resize = cv2.resize(img_roi, None, fx=4, fy=4,
                            interpolation=cv2.INTER_CUBIC)

    img_cinza = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_cinza, 70, 255, cv2.THRESH_BINARY)

    cv2.imwrite("output/roi-ocr.png", img_binary)

    cv2.imshow("res", img_binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ocrImageRoiPlaca():
    img_roi = cv2.imread("output/roi-ocr.png")

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pytesseract.image_to_string(img_roi, lang="eng", config=config)

    return saida


def ocrGoogleVisionApi():

    with open("output/roi.png", "rb") as img_file:
        my_base64 = base64.b64encode(img_file.read())

    url = "https://vision.googleapis.com/v1/images:annotate?key=[API-KEY]"
    data = {
        'requests': [
            {
                'image': {
                    'content': my_base64.decode('utf-8')
                },
                'features': [
                    {
                        'type': 'TEXT_DETECTION'
                    }
                ]
            }
        ]
    }

    r = requests.post(url=url, data=json.dumps(data))

    texts = r.json()['responses'][0]['textAnnotations']

    results = []

    for t in texts:
        results.append(t['description'])

    return results


if __name__ == "__main__":

    source = "resource/carro4.jpg"

    # encontrarRoiPlaca(source)

    # preProcessamentoRoi()

    #text = ocrImageRoiPlaca()

    # showText(text)

    text = ocrGoogleVisionApi()

    showText(text)
