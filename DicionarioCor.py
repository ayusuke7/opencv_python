import numpy as np 

cores = {'branco':(255, 255, 255), 'azul':(255, 0, 0),'verde':(0, 255, 0),
         'laranja':(0, 102, 255), 'amarelo':(0, 255, 255),'vermelho':(0, 0, 255)}

min_amarelo = np.array([20, 100, 100],np.uint8)
max_amarelo = np.array([30, 255, 255],np.uint8)

min_vermelho = np.array([160,20,70], np.uint8)
max_vermelho = np.array([190,255,255], np.uint8)

min_azul = np.array([110, 50, 50], np.uint8)
max_azul = np.array([127, 255, 255], np.uint8)
