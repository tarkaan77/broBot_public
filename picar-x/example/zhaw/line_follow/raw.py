from picarx import Picarx
from time import sleep

px = Picarx()

px_power = 5
turn_angle = 18  # Winkel, um den sich die Räder beim Abbiegen drehen

def get_direction(grayscale_values):
    left, middle, right = grayscale_values
    threshold = 22  # Angepasster Schwellenwert

    if middle < threshold:
        return 'forward'
    elif left < threshold:
        return 'left'
    elif right < threshold:
        return 'right'
    else:
        return 'stop'

def main():
    try:
        while True:
            grayscale_values = px.get_grayscale_data()
            direction = get_direction(grayscale_values)
            print("Grayscale values:", grayscale_values, "Direction:", direction)

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
        print("Programm beendet.")

if __name__ == '__main__':
    main()
