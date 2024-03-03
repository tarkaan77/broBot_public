#!/usr/bin/python3
import time
from picarx import Picarx

def adjust_direction(px, grayscale_values):
    # Passt die Richtung an, indem der Sensor mit dem niedrigsten Wert ermittelt wird.
    left_value, middle_value, right_value = grayscale_values
    min_value = min(grayscale_values)
    if left_value == min_value:
        px.set_dir_servo_angle(10)  # Linie ist mehr links
    elif right_value == min_value:
        px.set_dir_servo_angle(-10)  # Linie ist mehr rechts
    else:
        px.set_dir_servo_angle(0)  # Linie ist in der Mitte oder nicht erkennbar

def find_and_follow_line(px, px_power):
    # Findet und folgt der Linie basierend auf dem niedrigsten Sensorwert.
    grayscale_values = px.get_grayscale_data()
    print("Graustufen-Werte:", grayscale_values)

    if any(value < 50 for value in grayscale_values):  # Erhöhter Schwellenwert
        adjust_direction(px, grayscale_values)
        px.forward(px_power)
    else:
        # Keine Linie gefunden, weiterfahren und suchen
        px.forward(px_power)
        time.sleep(0.1)  # Kurz weiterfahren

def main():
    px = Picarx()
    px_power = 10

    try:
        while True:
            find_and_follow_line(px, px_power)
            time.sleep(0.1)
    finally:
        px.stop()

if __name__ == '__main__':
    main()
