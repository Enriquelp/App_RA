# Prueba de la camara web. Abre una ventana mostrando la imagen capturada de la camara web
# y se cierra al pulsar la tecla Q



import cv2

# Crea un objeto que representa la camara web
cap = cv2.VideoCapture(0) 

# Especificamos el algoritmo de compresion
fourcc = cv2.VideoWriter_fourcc(*'XVID') 

# Objeto para escribir el video en archivo con los parametros "ruta archivo destino", "algoritmo de compresion", "fotogramas por segundo" y "resolucion de imagen"
out = cv2.VideoWriter('Tests/PruebaVideo.avi', fourcc, 10.0, (640, 480)) #ruta del archivo destino, fotogramas por segundo y resolucion de imagen

while True:
    # Guarda en la variable booleana ret si se ha podido capturar imagen, y en frame un fotograma de la camara
    ret, frame = cap.read() 
    
    if ret:
        # Abre una ventana llamada Camara y muestra el frame
        cv2.imshow('Camara', frame)
        # Guarda el frame capturado 
        out.write(frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release() # libera el recurso, en este caso la camara web
out.release() 
cv2.destroyAllWindows() # cierra todas las ventanas