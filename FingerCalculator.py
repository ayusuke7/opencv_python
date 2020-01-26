import cv2
import numpy as np

min = np.array([110, 50, 50])
max = np.array([127, 255, 255])

kernel = np.ones((5, 5), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
line = cv2.LINE_AA

calculadora = [["9","8","7","/"],
               ["6","5","4","x"],
               ["3","2","1","-"],
               ["C","0","=","+"]]

coordenadas = []
motor = []

cap = cv2.VideoCapture(0)

def salvaCoordenadas(roi):

    alt, lar = roi.shape[:2]

    linhaV = int(lar / 4)
    linhaH = int(alt / 5)

    temp1 = []
    temp1.append((int(linhaV/2), int((linhaH)+(linhaH/2))))
    temp1.append((int(linhaV*2-linhaV/2), int((linhaH)+(linhaH/2))))
    temp1.append((int(linhaV*3-linhaV/2), int((linhaH)+(linhaH/2))))
    temp1.append((int(linhaV*4-linhaV/2), int((linhaH)+(linhaH/2))))

    temp2 = []
    temp2.append((int(linhaV/2), int((linhaH*2)+(linhaH/2))))
    temp2.append((int(linhaV*2-linhaV/2), int((linhaH*2)+(linhaH/2))))
    temp2.append((int(linhaV*3-linhaV/2), int((linhaH*2)+(linhaH/2))))
    temp2.append((int(linhaV*4-linhaV/2), int((linhaH*2)+(linhaH/2))))

    temp3 = []
    temp3.append((int(linhaV/2), int((linhaH*3)+(linhaH/2))))
    temp3.append((int(linhaV*2-linhaV/2), int((linhaH*3)+(linhaH/2))))
    temp3.append((int(linhaV*3-linhaV/2), int((linhaH*3)+(linhaH/2))))
    temp3.append((int(linhaV*4-linhaV/2), int((linhaH*3)+(linhaH/2))))

    temp4 = []
    temp4.append((int(linhaV/2), int((linhaH*4)+(linhaH/2))))
    temp4.append((int(linhaV*2-linhaV/2), int((linhaH*4)+(linhaH/2))))
    temp4.append((int(linhaV*3-linhaV/2), int((linhaH*4)+(linhaH/2))))
    temp4.append((int(linhaV*4-linhaV/2), int((linhaH*4)+(linhaH/2))))

    coordenadas.append(temp1)
    coordenadas.append(temp2)
    coordenadas.append(temp3)
    coordenadas.append(temp4)

    print("salvou")

def desenhaCalculadora(roi):

    alt, lar = roi.shape[:2]
    color = [0, 0, 255]

    linhaV = int(lar/4)
    linhaH = int(alt/5)

    #Desenha os Digitos de acordo com as coordenadas
    if len(coordenadas) == 4:
        for i in range(len(coordenadas)):
            for j in range(len(coordenadas[i])):
                cv2.circle(roi, coordenadas[i][j], 25, color, 2)

                #centraliza o texto -10 e +10
                x = coordenadas[i][j][0]
                y = coordenadas[i][j][1]
                cv2.putText(roi, calculadora[i][j], (x-10, y+10), font, 1, [255, 0, 0], 2, line)

    else:
        salvaCoordenadas(roi)

    #Desenha Linhas e Area de calculo da Calculadora
    cv2.rectangle(roi, (2, 2), (lar - 2, alt - 2), color, 2)
    cv2.line(roi, (linhaV*3, linhaH), (linhaV*3, alt), color, 2)
    cv2.line(roi, (0, linhaH),   (lar, linhaH  ), color, 2)

    #Motor Lexico
    if len(motor) > 0:

        pos = (int(linhaV*4-linhaV/2)-10, int((linhaH+10)-(linhaH/2)))

        if len(motor) == 1:
            view = motor[0]
        if len(motor) == 2:
            pos = (int(linhaV*4-linhaV/2)-60, int((linhaH+10)-(linhaH/2)))
            view = motor[0]+" "+motor[1]
        if len(motor) == 3:
            pos = (int(linhaV*4-linhaV/2)-80, int((linhaH+10)-(linhaH/2)))
            view = motor[0]+" "+motor[1]+" "+motor[2]
        if len(motor) == 4:
            view = motor[3]

        cv2.putText(roi, view, pos, font, 1, [0, 255, 255], 2, line)

def realizaCalculo():

    if motor[1] == "/": return int(motor[0]) / int(motor[2])
    if motor[1] == "x": return int(motor[0]) * int(motor[2])
    if motor[1] == "-": return int(motor[0]) - int(motor[2])
    if motor[1] == "+": return int(motor[0]) + int(motor[2])

    return "ER"

def selecionaValor(posicao):

    tam = len(motor)

    if  tam == 0 or tam == 2:
        #Digitos
        if posicao == coordenadas[0][0]: motor.append(calculadora[0][0])
        if posicao == coordenadas[0][1]: motor.append(calculadora[0][1])
        if posicao == coordenadas[0][2]: motor.append(calculadora[0][2])

        if posicao == coordenadas[1][0]: motor.append(calculadora[1][0])
        if posicao == coordenadas[1][1]: motor.append(calculadora[1][1])
        if posicao == coordenadas[1][2]: motor.append(calculadora[1][2])

        if posicao == coordenadas[2][0]: motor.append(calculadora[2][0])
        if posicao == coordenadas[2][1]: motor.append(calculadora[2][1])
        if posicao == coordenadas[2][2]: motor.append(calculadora[2][2])

        if posicao == coordenadas[3][1]: motor.append(calculadora[3][1])

    if tam == 1:
        # Operadores Aritimeticos
        if posicao == coordenadas[0][3]: motor.append(calculadora[0][3])
        if posicao == coordenadas[1][3]: motor.append(calculadora[1][3])
        if posicao == coordenadas[2][3]: motor.append(calculadora[2][3])
        if posicao == coordenadas[3][3]: motor.append(calculadora[3][3])

    if tam == 3:
        # Operador de igual
        if posicao == coordenadas[3][2]: motor.append(str(realizaCalculo()))

    if tam > 0 and tam <= 4:
        # Limpa o motor de calculo
        if posicao == coordenadas[3][0]: motor.clear()

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    alt, lar = frame.shape[:2]

    width  = int(lar/2)
    height = int(alt/2)+80

    roi = frame[0:width, height:lar]

    # Converte o espaco de cores RGB << HSV
    hsv  = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, min, max)

    open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)

    img, contours, hier = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        #Desenha retangulo
        #x, y, w, h = cv2.boundingRect(cnt)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        if radius < 50:
            posicao = (int(cx), int(cy))
            raio = int(radius)
            cv2.circle(roi, posicao, 25, (0, 255, 255), -1)
            text = "pos: " + str(posicao)
            cv2.putText(frame, text, (10, int(alt-20)), font, 1, (255, 255, 255), 2, line)
            selecionaValor(posicao)

    desenhaCalculadora(roi)

    cv2.imshow('frame', frame)
    #cv2.imshow('open', open)
    #cv2.imshow('close', close)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
