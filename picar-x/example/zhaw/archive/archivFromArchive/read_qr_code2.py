from time import sleep
from robot_hat import Music, TTS
import readchar
import cv2

# Initialisierung
music = Music()
tts = TTS()
tts.lang("en-US")
music.music_set_volume(20)

# Kamera initialisieren
cap = cv2.VideoCapture(0)

# Überprüfen, ob die Kamera korrekt initialisiert wurde
if not cap.isOpened():
    print("Failed to open camera")
    exit(1)

# QR-Code-Erkennungsfunktion
def scan_qr_code():
    # Versuchen, ein Bild aufzunehmen
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        return None

    # QR-Code-Erkennung
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)

    return data

# Hauptfunktion
def main():
    print("Press 's' to scan QR code, 'q' to play/stop music, SPACE for sound effect, 't' for text to speech.")
    
    flag_bgm = False

    while True:
        key = readchar.readkey()
        key = key.lower()

        if key == "q":
            flag_bgm = not flag_bgm
            if flag_bgm:
                music.music_play('../musics/slow-trail-Ahjay_Stelino.mp3')
            else:
                music.music_stop()

        elif key == readchar.key.SPACE:
            music.sound_play('../sounds/car-double-horn.wav')
            sleep(0.05)

        elif key == "t":
            words = "Hello"
            tts.say(words)

        elif key == "s":  # 's' für 'scan'
            print("Scanning QR Code...")
            qr_data = scan_qr_code()
            if qr_data in ["Zimmer 212", "Zimmer 216", "Zimmer 218"]:
                print(f"QR Code found: {qr_data}")
                music.sound_play('../sounds/success_tone.wav')
                tts.say(f"{qr_data} gefunden")
            else:
                print("QR Code not recognized or wrong room")
                tts.say("QR-Code nicht erkannt oder falscher Raum")

    # Kamera freigeben, wenn das Programm beendet wird
    cap.release()

if __name__ == "__main__":
    main()
