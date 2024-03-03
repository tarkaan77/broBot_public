import cv2
import numpy as np
from picarx import Picarx

def find_line(frame):
    # Konvertieren Sie das Bild zu Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wenden Sie einen binären Schwellenwert an, um die Linie zu isolieren
    _, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)

    # Finden Sie Konturen im Bild
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Finden Sie die größte Kontur, die die Linie repräsentieren könnte
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour
    return None

def main():
    px = Picarx()
    cap = cv2.VideoCapture(0) # Stellen Sie sicher, dass dies der korrekte Kamera-Index ist
    px_power = 10
    offset = 20

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            line_contour = find_line(frame)

            if line_contour is not None:
                # Berechnen Sie den Mittelpunkt der Linie
                M = cv2.moments(line_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Linienverfolgungslogik
                    frame_center = frame.shape[1] // 2
                    if cx < frame_center - 20: # Linie ist links
                        px.set_dir_servo_angle(offset)
                    elif cx > frame_center + 20: # Linie ist rechts
                        px.set_dir_servo_angle(-offset)
                    else: # Linie ist zentral
                        px.set_dir_servo_angle(0)

                    px.forward(px_power)
                else:
                    px.stop()
            else:
                px.stop()

    finally:
        px.stop()
        cap.release()

if __name__ == '__main__':
    main()
import cv2
import numpy as np
from picarx import Picarx

def find_line(frame):
    # Konvertieren Sie das Bild zu Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wenden Sie einen binären Schwellenwert an, um die Linie zu isolieren
    _, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)

    # Finden Sie Konturen im Bild
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Finden Sie die größte Kontur, die die Linie repräsentieren könnte
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour
    return None

def main():
    px = Picarx()
    cap = cv2.VideoCapture(0) # Stellen Sie sicher, dass dies der korrekte Kamera-Index ist

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            line_contour = find_line(frame)

            if line_contour is not None:
                # Berechnen Sie den Mittelpunkt der Linie
                M = cv2.moments(line_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                    # Linienverfolgungslogik
                    frame_center = frame.shape[1] // 2
                    if cx < frame_center - 20: # Linie ist links
                        px.set_dir_servo_angle(20)
                    elif cx > frame_center + 20: # Linie ist rechts
                        px.set_dir_servo_angle(-20)
                    else: # Linie ist zentral
                        px.set_dir_servo_angle(0)

                    px.forward(30)
                else:
                    px.stop()
            else:
                px.stop()

            # Anzeigen des Bildes für Debugging-Zwecke
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        px.stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

