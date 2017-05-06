"""
Contains all of the code necessary for starting, running, and maintaining ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dlamarca@uw.edu
    :GitHub: https://github.com/GhoulPoP/ProjectScarberry
    :Date: 26/7/2016 - 5/5/2017
    :cvar SETTINGS_FILE_DIRECTORY: The directory of ScarberrySettings.
    :type SETTINGS_FILE_DIRECTORY: type
    :cvar abort: Boolean used to test whether or not to abort the current session.
    :type abort: bool
    :cvar session_count: Counts the number of times the threads have been run
    :cvar type: int
    :class ThreadTrigger: An object which contains, manipulates, and returns booleans for thread activation and syncing.
    :function get_settings_dict: Returns a dictionary of dictionaries containing all of the values in ScarberrySettings.
    :function save_settings: Rewrites ScarberrySettings to a new dictionary of values.
    :function format_values_to_save: Formats one subdictionary to write over a part of ScarberrySettings.
    :function arduino_worker: The thread worker used to start, format, and end communication with the Arduino integral for the operation of ProjectScarberry.
    :function camera_worker: The thread worker used to start, format, and end communication with the Ximea camera integral for the operation of ProjectScarberry.
    :function process_worker: The thread worker used save and analyze the pictures from CameraThread.
    :function start_threads: Starts all of the different threads used to control the different parts of ProjectScarberry.
    :function abort_session: Terminates the workers in Main.
    :function main: Starts ProjectScarberry, loading the settings from ScarberrySettings, and evaluates whether or not to use ScarberryGui.
"""
import ArduinoController
import ProcessImage
import XimeaController
import time
import Queue
import threading
import Interface
import os

SETTINGS_FILE_DIRECTORY = 'ScarberrySettings'
abort = False
session_count  = -1

def get_settings_dict(keys):
    """
    Returns a dictionary of dictionaries containing all of the values in ScarberrySettings.
        :argument keys: A list containing the names of the different kinds of settings in ScarberrySettings.
        :type keys: list
        :return: All of the values in ScarberrySettings.
        :rtype: dict
    """
    settings_dic = {}
    for key in keys:
        settings_dic[key] = {}
    try:
        with open(SETTINGS_FILE_DIRECTORY) as file:
            print('Collecting {} information:'.format(file.name))
            for line in file.readlines():
                sub_dict = line[:line.index(':')]
                sub_key = line[line.index(':') + 1:line.index('[')]
                value = line[line.index('[') + 1:line.index(']')]
                settings_dic[sub_dict][sub_key] = value
            print settings_dic
    except IOError:
        settings_dic['Main']['UseInterface'] = 1
        settings_dic['Main']['RunTime'] = 0
        settings_dic['Arduino']['DutyCycle'] = '0.0'
        settings_dic['Arduino']['StrobeCount'] = 0
        settings_dic['Arduino']['FrameRate'] = 0
        settings_dic['Arduino']['SerialPort'] = 0
        settings_dic['XimeaController']['Gain'] = 0
        settings_dic['ProcessImage']['DrawColour'] = 0
        settings_dic['ProcessImage']['BaseName'] = ''
        settings_dic['ProcessImage']['BlurValue'] = 3
        settings_dic['ProcessImage']['FileExtension'] = '.TIF'
        settings_dic['ProcessImage']['ThreshLimit'] = 0
        settings_dic['ProcessImage']['DrawCentroid'] = 0
        settings_dic['ProcessImage']['SaveImage'] = 0
        settings_dic['ProcessImage']['NumberPadding'] = 0
        settings_dic['ProcessImage']['DrawROIs'] = 0
        settings_dic['ProcessImage']['DrawCount'] = 0
        settings_dic['ProcessImage']['ImageDirectory'] = 'images'
        save_settings(settings_dic)
    return settings_dic

def save_settings(settings):
    """
    Rewrites ScarberrySettings to a new dictionary of values.
        :argument settings: The replacement dictionary of subdictionaries containing settings.
        :type settings: dict
    """
    filename = SETTINGS_FILE_DIRECTORY
    file = open(filename, 'w')
    file.truncate()
    file.write(format_values_to_save("Main",settings.get("Main")))
    file.write(format_values_to_save("Arduino", settings.get("Arduino")))
    file.write(format_values_to_save("XimeaController", settings.get("XimeaController")))
    file.write(format_values_to_save("ProcessImage", settings.get("ProcessImage")))
    file.close()

def format_values_to_save(key,dict):
    """
    Formats one subdictionary to write over a part of ScarberrySettings.
        :argument key: The key of the subdictionary for labelling and identification.
        :type key: string
        :argument dict: The dictionary to be formatted.
        :type dict: dict
        :return: Formatted string of all of the settings in dict.
        :rtype: string
    """
    output = ""
    sub_keys = dict.keys()
    for sub_key in sub_keys:
        output += '{}:{}[{}]\n'.format(key,sub_key,dict.get(sub_key))
        print output
    return output

def arduino_worker(arduino_values,main_values,trigger,gui=None):
    """
    The thread worker used to start, format, and end communication with the Arduino integral for the operation of ProjectScarberry.
        :argument arduino_values: All of the Arduino settings in ScarberrySettings.
        :type arduino_values: dict
        :argument main_values: All of the Main settings in ScarberrySettings.
        :type main_values: dict
        :argument trigger: The ThreadTrigger which contains all of the booleans for thread syncing.
        :type trigger: ThreadTrigger
        :keyword gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
    """
    global abort
    wait = True
    controller = ArduinoController.ArduinoController(arduino_values.get("SerialPort"),gui=gui)
    if not abort:
        controller.write_value(arduino_values.get("FrameRate"))
        controller.write_value(arduino_values.get("StrobeCount"))
        controller.write_value(arduino_values.get("DutyCycle"))
    while not trigger.get(name='startArduino') and wait:
        if abort:
            wait = False
    if not abort:
        controller.write_value(1)
        trigger.set_on('startCamera')
        time.sleep(float(main_values.get("RunTime"))+1)
        controller.write_value(4)
        trigger.set_off('startCamera')
    Interface.choose_print(gui, 'arduino', 'ArduinoThread: Finished')

def camera_worker(queue,camera_values,arduino_values,trigger,gui=None):
    """
    The thread worker used to start, format, and end communication with the Ximea camera integral for the operation of ProjectScarberry.
        :argument queue: The queue used to store all of the pictures recieved from XimeaController.
        :type queue: Queue.Queue
        :argument camera_values: All of the XimeaController settings in ScarberrySettings.
        :type camera_values: dict
        :argument arduino_values: All of the Arduino settings in ScarberrySettings.
        :type arduino_values: dict
        :argument trigger: The ThreadTrigger which contains all of the booleans for thread syncing.
        :type trigger: ThreadTrigger
        :keyword gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
    """
    global abort
    camera = XimeaController.XimeaCamera(arduino_values.get("FrameRate"),
                                         gain=camera_values.get("Gain"),
                                         gui=gui)
    wait = True
    trigger.set_on('startArduino')
    while not trigger.get(name='startCamera') and wait:
        if abort:
            wait = False
    if not abort:
        camera.start_acquisition()
        while trigger.get(name='startCamera') and not abort:
            current_image = camera.get_image()
            queue.put(current_image)
        camera.stop_acquisition()
        trigger.set_off('runProcess')
    Interface.choose_print(gui, 'camera', 'CameraThread: Finished')

def save_worker(save_queue, data_queue, process_values, trigger, session_count, gui=None):
    """
    The thread worker used save and analyze the pictures from CameraThread.
        :argument queue: The queue used to store all of the pictures recieved from XimeaController.
        :type queue: Queue.Queue
        :argument process_values: All of the ProcessImage settings in ScarberrySettings.
        :type process_values: dict
        :argument trigger: The ThreadTrigger which contains all of the booleans for thread syncing.
        :type trigger: ThreadTrigger
        :argument session_count: The number of the current instance of the threads
        :type session_count: int
        :keyword gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
    """
    global abort
    pic_count = 0
    while trigger.get(name='runProcess') and not abort:
        while not save_queue.empty() and not abort:
            pic = save_queue.get()
            Interface.choose_print(gui, 'save', 'pic {} hex: {}'.format(pic_count,pic))
            formated_number = ProcessImage.format_number(pic_count,int(process_values.get("NumberPadding")))
            save_name = process_values.get("BaseName")
            if process_values.get("Count") > 0:
                save_name = '{}.{}'.format(save_name,session_count)
            ProcessImage.save_image(pic,
                                    formated_number,
                                    image_direcoty=process_values.get("ImageDirectory"),
                                    name=save_name,
                                    extention=process_values.get("FileExtension"))
            data_queue.put(pic)
            pic_count += 1
    trigger.set_off('runData')
    Interface.choose_print(gui, 'save', 'SaveImageThread: Finished')

def data_worker(queue, process_values, trigger, session_count, gui=None):
    """
    The thread worker used save and analyze the pictures from CameraThread.
        :argument queue: The queue used to store all of the pictures recieved from XimeaController.
        :type queue: Queue.Queue
        :argument process_values: All of the ProcessImage settings in ScarberrySettings.
        :type process_values: dict
        :argument trigger: The ThreadTrigger which contains all of the booleans for thread syncing.
        :type trigger: ThreadTrigger
        :argument session_count: The number of the current instance of the threads
        :type session_count: int
        :keyword gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
    """
    global abort
    pic_count = 0
    data_directory = process_values.get("ImageDirectory") + '\\data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    while trigger.get(name='runData') and not abort:
        while not queue.empty() and not abort:
            pic = queue.get()
            Interface.choose_print(gui, 'data', 'pic {} hex: {}'.format(pic_count, pic))
            formated_number = ProcessImage.format_number(pic_count, int(process_values.get("NumberPadding")))
            save_name = process_values.get("BaseName")
            if process_values.get("Count") > 0:
                save_name = '{}.{}'.format(save_name, session_count)
            data_filename = '{}\\data-{}_{}{}'.format(data_directory,
                                                      save_name,
                                                      formated_number,
                                                      '.txt')
            if process_values.get("SaveDraw"):
                ProcessImage.draw_and_data(pic,
                                           '{}\\data\\data-{}_{}{}'.format(process_values.get("ImageDirectory"),
                                                                           save_name,
                                                                           formated_number,
                                                                           process_values.get("FileExtension")),
                                           data_filename,
                                           process_values.get("BlurValue"),
                                           process_values.get("ThreshLimit"),
                                           draw_rois=process_values.get("DrawROIs"),
                                           draw_centroid=process_values.get("DrawCentroid"),
                                           draw_colours=process_values.get("DrawColour"),
                                           draw_count=process_values.get("DrawCount"))
            else:
                data = ProcessImage.get_data(pic,
                                             process_values.get("BlurValue"),
                                             process_values.get("ThreshLimit"))
                ProcessImage.save_data(data, data_filename)
            pic_count += 1
    Interface.choose_print(gui, 'data', 'DataImageThread: Finished')

def start_threads(settings,gui=None):
    """
    Starts all of the different threads used to control the different parts of ProjectScarberry.
        :argument settings: All of the settings contained in ScarberrySettings.
        :type settings: dict
        :keyword gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
    """
    global abort
    global session_count
    arduino_values = settings.get("Arduino")
    main_values = settings.get("Main")
    save_pic_queue = Queue.Queue(maxsize=0)
    data_pic_queue = Queue.Queue(maxsize=0)
    trigger_master = ThreadTrigger()
    trigger_master.register('startArduino',False)
    trigger_master.register('startCamera', False)
    trigger_master.register('runProcess', True)
    trigger_master.register('runData',True)
    trigger_master.register('runCamera', True)
    abort = False
    if settings.get("ProcessImage").get("Count") > 0:
        session_count += 1
    arduino = threading.Thread(name="ArduinoThread",
                               target=arduino_worker,
                               args=(arduino_values,
                                     main_values,
                                     trigger_master,),
                               kwargs={'gui':gui})
    camera = threading.Thread(name="CameraThread",
                              target=camera_worker,
                              args=(save_pic_queue,settings.get("XimeaController"),
                                    arduino_values,
                                    trigger_master),
                              kwargs={'gui':gui})
    save = threading.Thread(name="SaveImageThread",
                               target=save_worker,
                               args=(save_pic_queue,
                                     data_pic_queue,
                                     settings.get("ProcessImage"),
                                     trigger_master,
                                     session_count),
                               kwargs={'gui':gui})
    data = threading.Thread(name="DataImageThread",
                            target=data_worker,
                            args=(data_pic_queue,
                                  settings.get("ProcessImage"),
                                  trigger_master,
                                  session_count),
                            kwargs={'gui': gui})
    arduino.start()
    camera.start()
    save.start()
    data.start()

def abort_session():
    """
    Terminates the workers in Main.
    """
    global abort
    abort = True

def main():
    """
    Starts ProjectScarberry, loading the settings from ScarberrySettings, and evaluates whether or not to use ScarberryGui.
    """
    print help(ArduinoController.ArduinoController.write_value)
    settings = get_settings_dict(['Main','Arduino','XimeaController','ProcessImage'])
    if(int(settings.get("Main").get("UseInterface")) > 0):
        gui = Interface.ScarberryGui()
        gui.set_inputs(settings)
        gui.start()
    else:
        start_threads(settings)

class ThreadTrigger:
    """
    An object which contains, manipulates, and returns booleans for thread activation and syncing.
        :ivar __trigger_dic: The datastructure used to hold all of the booleans.
        :type __trigger_dic: dict
        :function register: Creates and registers a new trigger.
        :function toggle: Makes a triggers state toggle from on to off or from off to on.
        :function set_on: Sets a toggles state to on.
        :function set_off: Sets a toggles state to off.
        :function get: Returns the state of a trigger.
    """
    __trigger_dic = None

    def __init__(self):
        """
        Initializes an instance of ThreadTrigger.
        """
        self.__trigger_dic = {}

    def register(self, name, state):
        """
        Creates and registers a new trigger.
            :argument name: The key/name of the new trigger.
            :type name: string
            :argument state: Whether or not the new trigger is initialized as on or off.
            :type state: boolean
        """
        self.__trigger_dic[name] = state

    def toggle(self, name):
        """
        Makes a triggers state toggle from on to off or from off to on.
            :argument name:  The key/name of the trigger.
            :type name: string
        """
        try:
            self.__trigger_dic[name] = not self.__trigger_dic[name]
        except KeyError as key_err:
            print key_err

    def set_on(self, name):
        """
        Sets a toggles state to on.
            :argument name: The key/name of the trigger.
            :type name: string
        """
        try:
            self.__trigger_dic[name] = True
        except KeyError as key_err:
            print key_err

    def set_off(self, name):
        """
        Sets a toggles state to off.
            :argument name: The key/name of the trigger.
            :type name: string
        """
        try:
            self.__trigger_dic[name] = False
        except KeyError as key_err:
            print key_err

    def get(self, name=''):
        """
        Returns the state of a trigger.
            :argument name: The key/name of the trigger.
            :type name: string
            :return: The state of the trigger
            :rtype: boolean
        """
        try:
            if name != '':
                return self.__trigger_dic[name]
            else:
                return self.__trigger_dic
        except KeyError as key_err:
            print key_err

if __name__ == "__main__":
    main()

