import cv2

video = cv2.VideoCapture(1)
classificadorFaces = cv2.CascadeClassifier('cascades\\haarcascade_frontalface_default.xml')
classificadorOlhos = cv2.CascadeClassifier('cascades\\haarcascade_eye.xml');

while True:

    conectado, frame = video.read()

    frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = classificadorFaces.detectMultiScale(frameCinza, minSize=(70,70))

    for (x, y, l, a) in faces:
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 0), 2)
        olhos = classificadorOlhos.detectMultiScale(frameCinza)
        for(ox, oy, ol, oa) in olhos:
           cv2.rectangle(frame, (ox, oy), (ox + ol, oy + oa), (0, 0, 255), 2)

    cv2.imshow('Vídeo', frame)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()