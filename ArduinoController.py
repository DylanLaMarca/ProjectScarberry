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
    controller.write_value(10,sleep)
    controller.write_value(2,sleep)
    controller.write_value(.5,sleep)
    controller.write_value(1,sleep)
    controller.write_value(2,sleep)
    controller.write_value(3,sleep)
    time.sleep(1)
    controller.write_value(1,0)
if __name__ == "__main__":
    main()