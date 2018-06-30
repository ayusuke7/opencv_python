import cv2

img = cv2.imread('res/carros/carro (1).jpg')
cv2.imshow('img', img)

cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('cinza', cinza)

_, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
#cv2.imshow('bin', bin)

desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
cv2.imshow('des', desfoque)

_, contornos, hier = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#cv2.drawContours(img, contornos, -1, (0, 255, 0), 2)
#cv2.imshow('cont', img)

for c in contornos:
    perimetro = cv2.arcLength(c, True)
    if perimetro > 120:
        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
        if len(aprox) == 4:
            (x, y, alt, lar) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x+alt, y+lar), (0, 255, 0), 2)
            roi = img[y:y + lar, x:x + alt]
            cv2.imwrite('res/roi.jpg', roi)


cv2.imshow('draw', img)

cv2.waitKey(0)
cv2.destroyAllWindows()