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
        Interface.choose_print(gui, 'arduino', 'Waiting for COM{}...'.format(com_number))
        time.sleep(self.initial_sleep);
        Interface.choose_print(gui, 'arduino', 'Connected to COM{}.'.format(com_number))

    def write_value(self,value,pause):
        Interface.choose_print(self.gui, 'arduino', 'Writing "{}"...'.format(value))
        self.ser.write('{}'.format(value))
        time.sleep(pause)
        Interface.choose_print(self.gui, 'arduino', 'Wrote: {}'.format(value))