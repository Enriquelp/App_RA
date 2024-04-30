# Prueba de lectura de video

import cv2

# Especifica la ruta completa del archivo de video
ruta_video = 'Tests/PruebaVideo.avi'

# Crea un objeto VideoCapture para leer el archivo de video
cap = cv2.VideoCapture(ruta_video)

# Verifica si la apertura del archivo de video fue exitosa
if not cap.isOpened():
    print("Error al abrir el archivo de video")
    exit()

while True:
    # Lee un fotograma del archivo de video
    ret, frame = cap.read()

    # Verifica si se ha alcanzado el final del video
    if not ret:
        break

    # Muestra el fotograma en una ventana
    cv2.imshow('Video', frame)


    # Si se presiona la tecla 'q', se rompe el bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra la ventana
cap.release()
cv2.destroyAllWindows()
