from pydoc import text
from vilib import Vilib
from time import sleep, time, strftime, localtime
import threading
import readchar
import os
from robot_hat import Music, TTS

# Initialisierung von TTS und Musik
music = Music()
tts = TTS()
tts.lang("en-US")

flag_face = False
flag_color = False
qr_code_flag = False

qr_code_to_match = "Zimmer 212"  # Setzen Sie hier Ihren vorgegebenen String ein

manual = '''
Input key to call the function!
    q: Take photo
    1: Color detect : red
    2: Color detect : orange
    3: Color detect : yellow
    4: Color detect : green
    5: Color detect : blue
    6: Color detect : purple
    0: Switch off Color detect
    r: Scan the QR code
    f: Switch ON/OFF face detect
    s: Display detected object information
'''

color_list = ['close', 'red', 'orange', 'yellow',
              'green', 'blue', 'purple',
             ]

def face_detect(flag):
    print("Face Detect: " + str(flag))
    Vilib.face_detect_switch(flag)

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

def take_photo():
    _time = strftime('%Y-%m-%d-%H-%M-%S', localtime(time()))
    name = 'photo_%s' % _time
    username = os.getlogin()

    path = f"/home/{username}/Pictures/"
    Vilib.take_photo(name, path)
    print('Photo saved as %s%s.jpg' % (path, name))

def object_show():
    global flag_color, flag_face

    if flag_color is True:
        if Vilib.detect_obj_parameter['color_n'] == 0:
            print('Color Detect: None')
        else:
            color_coordinate = (Vilib.detect_obj_parameter['color_x'], Vilib.detect_obj_parameter['color_y'])
            color_size = (Vilib.detect_obj_parameter['color_w'], Vilib.detect_obj_parameter['color_h'])
            print("[Color Detect] ", "Coordinate:", color_coordinate, "Size", color_size)

    if flag_face is True:
        if Vilib.detect_obj_parameter['human_n'] == 0:
            print('Face Detect: None')
        else:
            human_coordinate = (Vilib.detect_obj_parameter['human_x'], Vilib.detect_obj_parameter['human_y'])
            human_size = (Vilib.detect_obj_parameter['human_w'], Vilib.detect_obj_parameter['human_h'])
            print("[Face Detect] ", "Coordinate:", human_coordinate, "Size", human_size)

def main():
    global flag_face, flag_color, qr_code_flag
    qrcode_thread = None

    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    print(manual)

    while True:
        key = readchar.readkey()
        key = key.lower()

        if key == 'q':
            take_photo()

        elif key != '' and key in '0123456':
            index = int(key)
            if index == 0:
                flag_color = False
                Vilib.color_detect('close')
            else:
                flag_color = True
                Vilib.color_detect(color_list[index])
            print('Color detect: %s' % color_list[index])

        elif key == "f":
            flag_face = not flag_face
            face_detect(flag_face)

        elif key == "r":
            qr_code_flag = not qr_code_flag
            if qr_code_flag:
                if qrcode_thread is None or not qrcode_thread.is_alive():
                    qrcode_thread = threading.Thread(target=qrcode_detect)
                    qrcode_thread.setDaemon(True)
                    qrcode_thread.start()
            else:
                if qrcode_thread is not None and qrcode_thread.is_alive():
                    qrcode_thread.join()
                    print('QRcode Detect: close')

        elif key == "s":
            object_show()

        sleep(0.5)

if __name__ == "__main__":
    main()
