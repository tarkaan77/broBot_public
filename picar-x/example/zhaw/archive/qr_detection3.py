from time import sleep
from robot_hat import TTS
import threading
from vilib import Vilib
 
# Initialisierung von TTS
tts = TTS()
tts.lang("en-US")
 
qr_code_flag = True  # Startet sofort mit dem Scannen
zimmer_nummer = input("Bitte geben Sie die Zimmernummer ein: ")  # Hier geben Sie die Zimmernummer manuell ein
qr_code_to_match = f"Zimmer {zimmer_nummer}"  # Kombinierter String für den QR-Code
 
def qrcode_detect():
    global qr_code_flag
    Vilib.qrcode_detect_switch(True)
    print("Warten auf QR-Code")
 
    text = None
    while qr_code_flag:
        temp = Vilib.detect_obj_parameter['qr_data']
        if temp != "None" and temp != text:
            text = temp
            print('QR-Code: %s' % text)
 
            # Überprüfen, ob der gescannte QR-Code mit dem vorgegebenen String übereinstimmt
            if text == qr_code_to_match:
                tts.say("We are here")
                qr_code_flag = False  # Beendet das Scannen und das Programm
            else:
                tts.say("Not here and Tarkan is a Pitsch")
 
        sleep(0.5)
    Vilib.qrcode_detect_switch(False)
 
def main():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
 
    qrcode_thread = threading.Thread(target=qrcode_detect)
    qrcode_thread.setDaemon(True)
    qrcode_thread.start()
    qrcode_thread.join()  # Wartet auf das Ende des QR-Code-Scanning-Threads
 
    print("Programm beendet")
 
if __name__ == "__main__":
    main()
