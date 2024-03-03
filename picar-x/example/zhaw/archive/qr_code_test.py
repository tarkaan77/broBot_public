import cv2
import numpy as np
from robot_hat import Music, TTS

# Initialisierung
music = Music()
tts = TTS()
tts.lang("en-US")
music.music_set_volume(20)

def find_line(frame):
    # Konvertieren Sie das Bild zu Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wenden Sie einen binären Schwellenwert an, um die Linie zu isolieren
    _, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)

    # Finden Sie Konturen im Bild
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Zeichnen Sie die Konturen auf das Bild
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

def scan_qr_code(frame):
    # QR-Code-Erkennung
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)
    return data

def main():
    cap = cv2.VideoCapture(0)  # Stellen Sie sicher, dass dies der korrekte Kamera-Index ist

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        find_line(frame)

        # QR-Code scannen
        qr_data = scan_qr_code(frame)
        if qr_data in ["Zimmer 212", "Zimmer 216", "Zimmer 218"]:
            print(f"QR Code found: {qr_data}")
            music.sound_play('../sounds/success_tone.wav')
            tts.say(f"{qr_data} gefunden")

        # Zeigen Sie das Bild an
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
