import cv2
from ultralytics import YOLO

# Intenta usar /dev/video0, pero si no funciona, prueba /dev/video1
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(1)  # Cambia el índice si no se abre con 0
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara.")
        exit()

cap.set(3, 1280)  # Establecer el ancho
cap.set(4, 720)   # Establecer la altura

model = YOLO('/home/renann/Documentos/Varios/Master/data/models/best.pt')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el frame.")
        break

    # Realizar la predicción
    results = model.predict(frame, imgsz=640, conf=0.6)

    # Verificar si se encontraron resultados
    if results:
        for result in results:
            bboxes = result.boxes  # Acceder a las cajas de la predicción

        # Dibujar los resultados en la imagen
        annotated_frame = results[0].plot()  # Anotar la imagen

        # Mostrar la imagen anotada
        cv2.imshow('DETECCION DE OBJETOS', annotated_frame)

    t = cv2.waitKey(1)
    if t == 27:  # Si presionas 'ESC' para salir
        break

cap.release()
cv2.destroyAllWindows()


