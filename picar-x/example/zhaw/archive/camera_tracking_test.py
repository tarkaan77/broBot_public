import cv2
import numpy as np

def find_line(frame):
    # Konvertieren Sie das Bild zu Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wenden Sie einen binären Schwellenwert an, um die Linie zu isolieren
    _, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)

    # Finden Sie Konturen im Bild
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Zeichnen Sie die Konturen auf das Bild
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

def main():
    cap = cv2.VideoCapture(0) # Stellen Sie sicher, dass dies der korrekte Kamera-Index ist

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        find_line(frame)

        # Zeigen Sie das Bild an
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

