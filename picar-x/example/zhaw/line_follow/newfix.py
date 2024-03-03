from picarx import Picarx
from time import sleep

px = Picarx()
px.set_line_reference([74, 11, 89])

px_power = 10
offset = 20

def get_status(val_list):
    left, middle, right = val_list

    if left < 80 and right > 100:
        return 'left'
    elif right < 100 and left > 80:
        return 'right'
    elif middle < 90:
        return 'forward'
    else:
        return 'stop'

def main():
    try:
        while True:
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list: %s, %s" % (gm_val_list, gm_state))

            if gm_state == "stop":
                px.stop()
            elif gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state == 'left':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)
            elif gm_state == 'right':
                px.set_dir_servo_angle(offset)
                px.forward(px_power)
            sleep(0.1)

    finally:
        px.stop()
        print("Stop and exit")

if __name__ == '__main__':
    main()
