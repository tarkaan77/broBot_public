from time import sleep
from robot_hat import TTS
import threading
import readchar
from vilib import Vilib

# Initialisierung von TTS
tts = TTS()
tts.lang("en-US")

qr_code_flag = False
qr_code_to_match = "Zimmer 212"  # Setzen Sie hier Ihren vorgegebenen String ein

def qrcode_detect():
    global qr_code_flag
    if qr_code_flag == True:
        Vilib.qrcode_detect_switch(True)
        print("Warten auf QR-Code")

    text = None
    while True:
        temp = Vilib.detect_obj_parameter['qr_data']
        if temp != "None" and temp != text:
            text = temp
            print('QR-Code: %s' % text)

            # Überprüfen, ob der gescannte QR-Code mit dem vorgegebenen String übereinstimmt
            if text == qr_code_to_match:
                tts.say("We are here")
            else:
                tts.say("Not here and Tarkan is a Pitsch")

        if qr_code_flag == False:
            break
        sleep(0.5)
    Vilib.qrcode_detect_switch(False)

def main():
    global qr_code_flag
    qrcode_thread = None

    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)

    while True:
        key = readchar.readkey()
        key = key.lower()

        if key == "r":
            qr_code_flag = not qr_code_flag
            if qr_code_flag:
                if qrcode_thread is None or not qrcode_thread.is_alive():
                    qrcode_thread = threading.Thread(target=qrcode_detect)
                    qrcode_thread.setDaemon(True)
                    qrcode_thread.start()
            else:
                if qrcode_thread is not None and qrcode_thread.is_alive():
                    qrcode_thread.join()
                    print('QR-Code-Erkennung beendet')

        sleep(0.5)

if __name__ == "__main__":
    main()
