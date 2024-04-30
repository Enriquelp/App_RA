# Aplicación RA

Se trata de una aplicación simple de realidad aumentada, haciendo uso de microservicios, en la cual se capturará video de una webcam y se mostrara en una pagina web ese video con una imagen superpuesta en 2 dimensiones.

# Microservicios / Tareas

- **Video Capturer:** Captura video por una cámara web. Solo imágenes, no se necesita audio. Hace uso de la libreria OpenCV orientada a la visión por computador.
  Se debe poder configurar la resolución (tamaño de la imagen), los FPS de captura y reproducción y el formato del video.

- **Video Generator:** Cumple la misma función que el Video Generator pero enviando un video pregrabado en bucle, facilitando la ejecución de la aplicación si no se dispone de webcam.

- **Feature Communicator:** Inicia la linea de detección de elementos (Codigos ArUco). Recibe el video y lo transforma a blanco y negro para enviárselo a la tarea de detección de elementos.

- **ArUco Tracker:** Busca códigos ArUco en el video recibido por el Feature Communicator, obteniendo sus identificadores y coordenadas asociadas para enviarlas al servidor de visualización.

- **Filter Selector:** inicia la linea de visualización, aplicando un filtro en tiempo de ejecución. Una vez completado, manda el video modificado al servidor de visualización.

- **Visualizer:** Recibe el video modificado (del Filter Selector) y el identificador con las coordenadas de ArUco (del ArUco Tracker) para realizar la representación de una imagen 2D en tiempo real. Si no recibe datos de los dos, muestra una imagen que indica que no hay señal.

# Dependencias

- [OpenCV](https://opencv.org/)
    - en Windows/Linux: `pip3 install opencv-python`
