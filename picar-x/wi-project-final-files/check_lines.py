from picarx import Picarx
import time

px = Picarx()

def test_sensors():
    while True:
        grayscale_values = px.get_grayscale_data()
        print("Grayscale values:", grayscale_values)
        time.sleep(0.5)

if __name__ == "__main__":
    test_sensors()


