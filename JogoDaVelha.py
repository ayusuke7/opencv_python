import cv2
import numpy as np

cap  = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
font = cv2.FONT_HERSHEY_SIMPLEX
line = cv2.LINE_AA

kernel_open  = np.ones((5, 5), np.uint8)
kernel_close = np.ones((20, 20), np.uint8)

jogadas = [" ", " ", " "," ", " ", " "," ", " ", " "]
coordenadas  = []

vez = "X"
msg = "JOGADOR DA VEZ => "

color_linhas = [0, 0, 255]
color_point  = [255, 255, 255]
color_jogad  = [0, 0, 255]

size_point = 10
size_jogad = 3

def salvaCoordenadas(alt, lar):

    linhaH1 = int(alt / 3)
    linhaV1 = int(lar / 3)

    coordenadas.append((int(linhaV1 / 2), int(linhaH1 / 2)))
    coordenadas.append((int(lar / 2), int(linhaH1 / 2)))
    coordenadas.append((int(lar - int(linhaV1 / 2)), int(linhaH1 / 2)))
    coordenadas.append((int(linhaV1 / 2), int(alt / 2)))
    coordenadas.append((int(lar / 2), int(alt / 2)))
    coordenadas.append((int(lar - int(linhaV1 / 2)), int(alt / 2)))
    coordenadas.append((int(linhaV1 / 2), int(alt - int(linhaH1 / 2))))
    coordenadas.append((int(lar / 2), int(alt - int(linhaH1 / 2))))
    coordenadas.append((int(lar - int(linhaV1 / 2)), int(alt - int(linhaH1 / 2))))

def desenhaTabuleiro(roi):

    alt, lar = roi.shape[:2]

    linhaH1 = int(alt / 3)
    linhaH2 = linhaH1 * 2
    linhaV1 = int(lar / 3)
    linhaV2 = linhaV1 * 2

    # Tabuleiro
    cv2.rectangle(roi, (2, 2), (lar-2, alt-2), color_linhas, 2)
    # linhas horizontais
    cv2.line(roi, (0, linhaH1), (lar, linhaH1), color_linhas, 2)
    cv2.line(roi, (0, linhaH2), (lar, linhaH2), color_linhas, 2)
    # linhas Verticais
    cv2.line(roi, (linhaV1, 0), (linhaV1, alt), color_linhas, 2)
    cv2.line(roi, (linhaV2, 0), (linhaV2, alt), color_linhas, 2)

    # Preenche o Vetor com as coordenadas dos Pontos na primeira interação
    if len(coordenadas) == 9:

        # Desenha as pontos ou as jogadas 1, 2, 3 de acordo com o vetor de Jogadas
        if jogadas[0] == " ":cv2.circle(roi, coordenadas[0], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[0], (20, 70), font, size_jogad, color_jogad, 2, line)
        if jogadas[1] == " ":cv2.circle(roi, coordenadas[1], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[1], ((linhaV1 + 20), 70), font, size_jogad, color_jogad, 2, line)
        if jogadas[2] == " ":cv2.circle(roi, coordenadas[2], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[2], ((linhaV2 + 20), 70), font, size_jogad, color_jogad, 2, line)

        # Desenha as pontos ou as jogadas 4, 5, 6 de acordo com o vetor de Jogadas
        if jogadas[3] == " ":cv2.circle(roi, coordenadas[3], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[3], (20, (linhaH1 + 72)), font, size_jogad, color_jogad, 2, line)
        if jogadas[4] == " ":cv2.circle(roi, coordenadas[4], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[4], ((linhaV1 + 20), (linhaH1 + 72)), font, size_jogad, color_jogad, 2, line)
        if jogadas[5] == " ":cv2.circle(roi, coordenadas[5], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[5], ((linhaV2 + 20), (linhaH1 + 72)), font, size_jogad, color_jogad, 2, line)

        # Desenha as pontos ou as jogadas 7, 8, 9 de acordo com o vetor de Jogadas
        if jogadas[6] == " ":cv2.circle(roi, coordenadas[6], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[6], (20, (linhaH2 + 72)), font, size_jogad, color_jogad, 2, line)
        if jogadas[7] == " ":cv2.circle(roi, coordenadas[7], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[7], ((linhaV1 + 20), (linhaH2 + 72)), font, size_jogad, color_jogad, 2, line)
        if jogadas[8] == " ":cv2.circle(roi, coordenadas[8], size_point, color_point, 2)
        else:cv2.putText(roi, jogadas[8], ((linhaV2 + 20), (linhaH2 + 72)), font, size_jogad, color_jogad, 2, line)

    else:
        salvaCoordenadas(alt, lar)

def verificaColisao(point):
    # Verifica se houve colisoes e atualiza o vetor de jogadas
    for i in range(len(coordenadas)):
        if coordenadas[i] == point and jogadas[i] == " ": jogadas[i] = alternaVez()

def verificaVencedor(roi):

    # Verifica o vetor de jogadas, caso tenha um vencedor mostra o Vencedor
    if jogadas[0] == jogadas[1] == jogadas[2] != " ":
        cv2.line(roi, coordenadas[0], coordenadas[2], color_jogad, 2)
        return True
    if jogadas[3] == jogadas[4] == jogadas[5] != " ":
        cv2.line(roi, coordenadas[3], coordenadas[5], color_jogad, 2)
        return True
    if jogadas[6] == jogadas[7] == jogadas[8] != " ":
        cv2.line(roi, coordenadas[6], coordenadas[8], color_jogad, 2)
        return True
    if jogadas[0] == jogadas[3] == jogadas[6] != " ":
        cv2.line(roi, coordenadas[0], coordenadas[6], color_jogad, 2)
        return True
    if jogadas[1] == jogadas[4] == jogadas[7] != " ":
        cv2.line(roi, coordenadas[1], coordenadas[7], color_jogad, 2)
        return True
    if jogadas[2] == jogadas[5] == jogadas[8] != " ":
        cv2.line(roi, coordenadas[2], coordenadas[8], color_jogad, 2)
        return True
    if jogadas[0] == jogadas[4] == jogadas[8] != " ":
        cv2.line(roi, coordenadas[0], coordenadas[8], color_jogad, 2)
        return True
    if jogadas[2] == jogadas[4] == jogadas[7] != " ":
        cv2.line(roi, coordenadas[2], coordenadas[7], color_jogad, 2)
        return True

    return False

def alternaVez():

    global vez

    temp = vez

    if vez == "X":
        vez = "O"
    else:
        vez = "X"

    return temp

while (cap.isOpened()):

    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)
    alt, lar = frame.shape[:2]

    #[ini_alt:fin_alt, ini_lar:fin_lar]
    roi = frame[0:int(alt/2), int(lar/2):lar]

    # MOG2 Background subtracao de fundo
    fgmask = roi
    fgbg.setBackgroundRatio(0.005)
    fgmask = fgbg.apply(roi, fgmask)
    #cv2.imshow('fgmask', fgmask)

    # erosão
    # 2x fechamento para remocao de ruidos
    erode  = cv2.erode(fgmask, kernel_open, iterations=1)
    open   = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel_open)
    close  = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel_close)
    cv2.imshow('closing', close)

    _, contours, hier = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Desenha o contorno da mao
    """for cnt in contours:
        cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)"""

    #end_point = None

    if contours:

        cnt = contours[0]
        moments = cv2.moments(cnt)# Procurar momentos de contorno

        cx = 0
        cy = 0

        # Envolve a mão com o Circulo
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        #if radius > 60 and radius < 150:
        cv2.circle(roi, (int(x), int(y)), int(radius), (0, 0, 0), 2)

        # Calcula o momento central da Mao
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
            cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00

        center = (cx, cy)
        cv2.circle(roi, center, 20, (0, 0, 255), 2) # Desenha um circulo no centro de massa da mao

        cnt     = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True) # Aproxima da forma correspondente
        hull    = cv2.convexHull(cnt, returnPoints=False) # verifica uma curva para defeitos de convexidade
        defects = cv2.convexityDefects(cnt, hull)

        if defects is not None:

            s, e, f, d = defects[0, 0]
            start = tuple(cnt[s][0])
            end   = tuple(cnt[e][0])

            # desenha linha a partir do centro >> ponta do dedo
            cv2.line(roi, center, end, [0, 0, 255], 2)
            cv2.circle(roi, end, size_point, [0, 0, 255], -1)

            # verifica as colisoes pontos com ponta do dedo
            verificaColisao(end)
            cv2.putText(frame, str(end), (lar - 170, alt - 20), font, 1, [0, 255, 255], 2, line)

    desenhaTabuleiro(roi)

    if verificaVencedor(roi) == True:
        msg = "PARABENS VOCE VENCEU"

    cv2.putText(frame, msg+vez, (10, alt - 20), font, 1, [0, 255, 255], 2, line)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

