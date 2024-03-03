from picarx import Picarx
import keyboard  # Importieren des keyboard-Moduls
from time import sleep

px = Picarx()
# manual modify reference value
px.set_line_reference([74, 11, 89])

px_power = 3
offset = 20

def get_status(val_list):
    _state = px.get_line_status(val_list)  # [bool, bool, bool], 0 means line, 1 means background
    if _state == [0, 0, 0]:
        return 'stop'
    elif _state[1] == 1:
        return 'forward'
    elif _state[0] == 1:
        return 'right'
    elif _state[2] == 1:
        return 'left'

def main():
    try:
        while True:
            if keyboard.is_pressed('q'):  # Beendet das Programm, wenn 'q' gedrückt wird
                print("Stoppt wegen Tastendruck.")
                break

            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list: %s, %s" % (gm_val_list, gm_state))

            if gm_state == "stop":
                px.stop()
            elif gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state == 'left':
                px.set_dir_servo_angle(offset)
                px.forward(px_power)
            elif gm_state == 'right':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)

    finally:
        px.stop()
        print("Stop and exit")

if __name__ == '__main__':
    main()
