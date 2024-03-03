#!/usr/bin/python3
import time
from picarx import Picarx

def adjust_direction(px, grayscale_values):
    """
    Passt die Richtung an, indem der Sensor mit dem niedrigsten Wert ermittelt wird.
    """
    left_value, middle_value, right_value = grayscale_values

    # Bestimme, welcher Sensor den niedrigsten Wert hat
    min_value = min(grayscale_values)
    if left_value == min_value:
        # Linie ist mehr links, also nach links steuern
        px.set_dir_servo_angle(10)
    elif right_value == min_value:
        # Linie ist mehr rechts, also nach rechts steuern
        px.set_dir_servo_angle(-10)
    else:
        # Linie ist entweder in der Mitte oder nicht erkennbar, also geradeaus fahren
        px.set_dir_servo_angle(0)

def find_and_follow_line(px, px_power):
    """
    Findet und folgt der Linie basierend auf dem niedrigsten Sensorwert.
    """
    grayscale_values = px.get_grayscale_data()
    print("Graustufen-Werte:", grayscale_values)

    # Überprüfe, ob ein Sensorwert signifikant niedrig ist (z.B. unter 25)
    if any(value < 25 for value in grayscale_values):
        adjust_direction(px, grayscale_values)
        px.forward(px_power)
    else:
        # Keine Linie gefunden, anhalten
        px.stop()

def main():
    px = Picarx()
    px_power = 5

    try:
        while True:
            find_and_follow_line(px, px_power)
            time.sleep(0.1)
    finally:
        px.stop()

if __name__ == '__main__':
    main()
