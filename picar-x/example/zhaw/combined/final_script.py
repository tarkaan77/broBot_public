from picarx import Picarx
from time import sleep
import threading
from robot_hat import TTS
from vilib import Vilib

px = Picarx()

px_power = 5
turn_angle = 18
qr_code_flag = True
zimmer_nummer = input("Bitte geben Sie die Zimmernummer ein: ")
qr_code_to_match = f"Zimmer {zimmer_nummer}"

tts = TTS()
tts.lang("en-US")

def get_direction(grayscale_values):
    left, middle, right = grayscale_values
    threshold = 22

    if middle < threshold:
        return 'forward'
    elif left < threshold:
        return 'left'
    elif right < threshold:
        return 'right'
    else:
        return 'stop'

def qrcode_detect():
    global qr_code_flag
    Vilib.qrcode_detect_switch(True)
    print("Warten auf QR-Code")

    while qr_code_flag:
        temp = Vilib.detect_obj_parameter['qr_data']
        if temp != "None":
            print('QR-Code: %s' % temp)

            if temp == qr_code_to_match:
                tts.say("We are here")
                qr_code_flag = False
            else:
                tts.say("This is the wrong place")

        sleep(0.5)
    Vilib.qrcode_detect_switch(False)

def main():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)

    qrcode_thread = threading.Thread(target=qrcode_detect)
    qrcode_thread.setDaemon(True)
    qrcode_thread.start()

    try:
        while qr_code_flag:
            grayscale_values = px.get_grayscale_data()
            direction = get_direction(grayscale_values)

            if direction == 'stop':
                px.stop()
            elif direction == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif direction == 'left':
                px.set_dir_servo_angle(-turn_angle)
                px.forward(px_power)
            elif direction == 'right':
                px.set_dir_servo_angle(turn_angle)
                px.forward(px_power)

            sleep(0.1)

    finally:
        px.stop()
        qrcode_thread.join()
        Vilib.camera_stop()
        Vilib.display_stop()
        print("Programm beendet")

if __name__ == "__main__":
    main()
