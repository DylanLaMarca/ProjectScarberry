"""
Contains all of the code needed to interact and utilize an Arduino for ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dylan@lamarca.org
    :GitHub: https://github.com/GhoulPoP/ProjectScarberry
    :Date: 28/7/2016 - 21/2/2016
    :class ArduinoController: An object used to establish and manage a connection with an Arduino connected via USB.
"""
import serial
import time
import Interface

class ArduinoController:
    """
    An object used to establish and manage a connection with an Arduino connected via USB.
        :cvar INITIAL_SLEEP: Amount of time in seconds the __init__ waits for the Serial to connect before continuing.
        :type INITUAL_SLEEP: int
        :ivar serial: Port number of the Arduino.
        :type serial: int
        :ivar gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
        :function write_value: Writes a value to the Arduino over Serial.
    """
    INITIAL_SLEEP = 2
    serial = None
    gui = None

    def __init__(self,com_number,gui=None):
        """
        Initializes an instance of ArduinoController.
            :argument com_number: Port number of the Arduino.
            :type com_number: int
            :keyword gui: Optional interface used to print(default None).
            :type gui: Interface.ScarberryGui
        """
        self.gui = gui
        self.serial = serial.Serial('COM{}'.format(com_number),115200)
        # Interface.choose_print(gui, 'arduino', 'Waiting for COM{}...'.format(com_number))
        print('Waiting for COM{}...'.format(com_number))
        time.sleep(ArduinoController.INITIAL_SLEEP);
        # Interface.choose_print(gui, 'arduino', 'Connected to COM{}.'.format(com_number))
        print('Connected to COM{}.'.format(com_number))

    def write_value(self,value):
        """
        Write a value to the Arduino over Serial.
            :argument value: Value to be written to Arduino
            :type value: string, int, float
            :argument pause: Amount of time spent paused in seconds
            :type pause: int, float
        """
        #Interface.choose_print(self.gui, 'arduino', 'Writing "{}"...'.format(value))
        print 'Writing "{}"...'.format(value)
        self.serial.write('{}'.format(value))
        self.serial.readline()
        #Interface.choose_print(self.gui, 'arduino', 'Wrote: {}'.format(value))
        print 'Wrote: {}'.format(value)

print(Interface.__file__)
controller = ArduinoController(3)
controller.write_value(10)
controller.write_value(5)
controller.write_value(.5)
controller.write_value(1)