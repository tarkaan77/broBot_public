#!/usr/bin/python3
import time
from picarx import Picarx
 
def calibrate_ref_value(px):
  """
  Kalibriert den Referenzwert fuer die Graustufenerkennung.
  """
  input("Platziere die Sensoren ueber der Linie und druecke Enter.")
  Ref = sum(px.get_grayscale_data()) / len(px.get_grayscale_data())
  print("Kalibrierter Referenzwert:", Ref)
  return Ref
 
def adjust_direction(px, grayscale_values, Ref):
  """
  Passt die Richtung an, um die Linie basierend auf allen Sensoren zu verfolgen.
  """
  left_value, middle_value, right_value = grayscale_values
 
   # Berechne den Fehler basierend auf Sensorwerten
  if left_value < Ref and right_value > Ref:
      # Linie ist mehr links, also nach links steuern
      px.set_dir_servo_angle(10)
  elif right_value < Ref and left_value > Ref:
      # Linie ist mehr rechts, also nach rechts steuern
      px.set_dir_servo_angle(-10)
  elif middle_value < Ref:
      # Linie ist in der Mitte, aber schwach, also geradeaus fahren
      px.set_dir_servo_angle(0)
  else:
      # Linie ist nicht klar erkennbar, Richtung beibehalten
      pass
 
def find_and_follow_line(px, Ref, px_power):
  """
  Findet und folgt der Linie.
  """
  grayscale_values = px.get_grayscale_data()
  print("Graustufen-Werte:", grayscale_values)
 
   # Ueberpruefe, ob sich die Sensoren ueber der Linie befinden
  if any(value < 300 for value in grayscale_values):
      adjust_direction(px, grayscale_values, Ref)
      px.forward(px_power)
      return True
  else:
      # Keine Linie gefunden, rueckwaerts fahren und suchen
      px.backward(px_power)
      time.sleep(0.5)  # Kurze Rueckwaertsfahrt
      px.stop()
      # Versuche, die Richtung anzupassen, um die Linie zu finden
      px.set_dir_servo_angle(-20)
      time.sleep(0.5)
      px.set_dir_servo_angle(20)
      time.sleep(0.5)
      px.set_dir_servo_angle(0)
      return False
 
def main():
  px = Picarx()
  Ref = calibrate_ref_value(px)
  px_power = 10
 
  try:
      while True:
          if not find_and_follow_line(px, Ref, px_power):
               print("Linie suchen...")
          time.sleep(0.1)
  finally:
      px.stop()
 
if __name__ == '__main__':
  main()
  
