import serial
import time

class ArduinoController:
    ser = None

    def __init__(self,com_number):
        self.ser = serial.Serial('COM{}'.format(com_number),9600)
        print('Waiting for COM{}...'.format(com_number))
        time.sleep(5);

    def write_value(self,value,pause):
        print('Writing "{}"...'.format(value))
        self.ser.write('{}'.format(value))
        time.sleep(pause)
        print('Wrote: {}'.format(value))

def main():
    controller = ArduinoController(6)
    controller.write_value(30,3)
    controller.write_value(.5,3)

if __name__ == "__main__":
    main()