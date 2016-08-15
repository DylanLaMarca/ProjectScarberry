import serial
import time
import Interface

class ArduinoController:
    initial_sleep = 2
    ser = None
    gui = None

    def __init__(self,com_number,gui):
        self.gui = gui
        self.ser = serial.Serial('COM{}'.format(com_number),115200)
        Interface.chose_print(gui,'arduino','Waiting for COM{}...'.format(com_number))
        time.sleep(self.initial_sleep);
        Interface.chose_print(gui,'arduino','Connected to COM{}.'.format(com_number))

    def write_value(self,value,pause):
        Interface.chose_print(self.gui,'arduino','Writing "{}"...'.format(value))
        self.ser.write('{}'.format(value))
        time.sleep(pause)
        Interface.chose_print(self.gui,'arduino','Wrote: {}'.format(value))

def main():
    sleep = 2
    controller = ArduinoController(6)
    controller.write_value(5, sleep)
    controller.write_value(6, sleep)
    controller.write_value(.5, sleep)
    controller.write_value(1, 0)

if __name__ == "__main__":
    main()