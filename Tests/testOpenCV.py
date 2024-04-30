# Al ejecutarse, abre una ventana mostrando la imagen seleccionada y 
# se cierra al presionar una tecla

import cv2 as cv

# Lee la imagen en la ruta seleccionada
img = cv.imread("imageTest.png") 
# Abre una ventana mostrando la imagen
cv.imshow("Display window", img) 
# Al pusar una tecla, la ventana se cierra
k = cv.waitKey(0) 