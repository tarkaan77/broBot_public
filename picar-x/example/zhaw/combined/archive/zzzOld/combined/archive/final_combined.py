from picarx import Picarx
from time import sleep
from robot_hat import TTS
import threading
from vilib import Vilib
import sys

# Initialisierung von TTS
tts = TTS()
tts.lang("en-US")

# Initialisierung von Picar-X
px = Picarx()
px_power = 10
turn_angle = 23  # Winkel, um den sich die Räder beim Abbiegen drehen

# QR-Code-Erkennung
qr_code_flag = False
zimmer_nummer = input("Bitte geben Sie die Zimmernummer ein: ")
qr_code_to_match = f"Zimmer {zimmer_nummer}"

def get_direction(grayscale_values):
    left, middle, right = grayscale_values
    threshold = 35  # Angepasster Schwellenwert

    if middle < threshold:
        return 'forward'
    elif left < threshold:
        return 'left'
    elif right < threshold:
        return 'right'
    else:
        return 'stop'

def line_tracking(stop_at_end=True):
    stop_counter = 0
    max_stop_count = 1  # Maximal erlaubte "Stop"-Signale in Folge

    try:
        while True:
            grayscale_values = px.get_grayscale_data()
            direction = get_direction(grayscale_values)
            print("Grayscale values:", grayscale_values, "Direction:", direction)

            if direction == 'stop':
                stop_counter += 1
                if stop_at_end and stop_counter >= max_stop_count:
                    px.stop()  # Stoppt den Roboter, bevor die Kamera aktiviert wird
                    break  # Beendet die Schleife, wenn der Schwellenwert erreicht ist
                sleep(1)  # Kurze Pause, um erneut zu prüfen
            else:
                stop_counter = 0  # Zurücksetzen des Zählers, wenn eine Linie erkannt wird
                if direction == 'forward':
                    px.set_dir_servo_angle(0)
                elif direction == 'left':
                    px.set_dir_servo_angle(-turn_angle)
                elif direction == 'right':
                    px.set_dir_servo_angle(turn_angle)
                px.forward(px_power)
            sleep(0.1)
    except KeyboardInterrupt:
        px.stop()
        sys.exit("Programm durch Benutzer gestoppt.")

def qrcode_detect():
    global qr_code_flag
    Vilib.qrcode_detect_switch(True)
    print("Warten auf QR-Code")

    try:
        while qr_code_flag:
            temp = Vilib.detect_obj_parameter['qr_data']
            if temp != "None":
                print('QR-Code: %s' % temp)

                if temp == qr_code_to_match:
                    tts.say("We are here")
                    qr_code_flag = False
                else:
                    tts.say("This is the wrong place")
                    qr_code_flag = False
                    sleep(2)  # Kurze Pause, bevor der Roboter weiterfährt
                    line_tracking(stop_at_end=False)  # Setzt die Linienverfolgung fort

            sleep(0.5)
    except KeyboardInterrupt:
        sys.exit("QR-Code-Erkennung durch Benutzer gestoppt.")
    finally:
        Vilib.qrcode_detect_switch(False)

def main():
    line_tracking()

    qr_code_flag = True
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)

    try:
        qrcode_thread = threading.Thread(target=qrcode_detect)
        qrcode_thread.setDaemon(True)
        qrcode_thread.start()
        qrcode_thread.join()
    except KeyboardInterrupt:
        sys.exit("Programm durch Benutzer gestoppt.")
    finally:
        # Vilib.camera_stop()  # Entfernt, falls die Methode nicht existiert
        Vilib.display_stop()
        print("Programm beendet")

if __name__ == "__main__":
    main()
