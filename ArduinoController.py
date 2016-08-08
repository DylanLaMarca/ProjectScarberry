import serial
import time

class ArduinoController:
    initial_sleep = 2
    ser = None

    def __init__(self,com_number):
        self.ser = serial.Serial('COM{}'.format(com_number),115200)
        print('Waiting for COM{}...'.format(com_number))
        time.sleep(self.initial_sleep);

    def write_value(self,value,pause):
        print('Writing "{}"...'.format(value))
        self.ser.write('{}'.format(value))
        time.sleep(pause)
        print('Wrote: {}'.format(value))

def main():
    sleep = 2
    controller = ArduinoController(6)
    controller.write_value(5,sleep)
    controller.write_value(.5,sleep)
    controller.write_value(6,sleep)

if __name__ == "__main__":
    main()