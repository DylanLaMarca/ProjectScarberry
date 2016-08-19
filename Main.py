import ArduinoController
import ProcessImage
import XimeaClient
import struct
import subprocess
import time
import Queue
import threading
import Interface

settings_file_directory = 'ScarberrySettings'

def get_settings_dic(keys):
    settings_dic = {}
    for key in keys:
        settings_dic[key] = []
    with open(settings_file_directory) as file:
        print('Collecting {} information:'.format(file.name))
        for line in file.readlines():
            settings_dic[line[:line.index(':')]].append(line[line.index('[') + 1:line.index(']')])
        print settings_dic
    return settings_dic

def save_settings(settings):
    filename = settings_file_directory
    file = open(filename, 'w')
    file.truncate()
    file.write(format_values_to_save("Main",settings.get("Main")))
    file.write(format_values_to_save("Arduino", settings.get("Arduino")))
    file.write(format_values_to_save("XimeaClient", settings.get("XimeaClient")))
    file.write(format_values_to_save("ProcessImage", settings.get("ProcessImage")))
    file.close()

def format_values_to_save(key,values):
    output = ""
    for value in values:
        output += '{}:[{}]\n'.format(key,value)
        print output
    return output

def arduino_worker(arduino_values,main_values,trigger,gui=None):
    controller = ArduinoController.ArduinoController(arduino_values[0], gui)
    for count in range(len(arduino_values)-1):
        controller.write_value(arduino_values[count+1], 2)
    while not trigger.get(name='startArduino'):
        pass
    controller.write_value(1,0)
    trigger.set_true('startCamera')
    time.sleep(float(main_values[1])+1)
    controller.write_value(4,0)
    Interface.choose_print(gui, 'arduino', 'ArduinoThread: Finished')

def camera_worker(queue,camera_values,arduino_values,trigger,gui=None):
    subprocess.Popen('XimeaController\\XimeaController\\bin\\Debug\\XimeaController.exe')
    time.sleep(6)
    try:
        client = XimeaClient.XimeaClient(arduino_values[1],camera_values[0], gui);
        run = True
        time.sleep(3)
        trigger.set_true('startArduino')
        while not trigger.get(name='startCamera'):
            pass
        while run:
            try:
                current_image = client.get_image()
                queue.put(current_image)
            except struct.error as struct_err:
                Interface.choose_print(gui, 'camera', 'Main: Server Disconnected: struct_err: {}'.format(struct_err))
                run = False
    except IOError as io_err:
        Interface.choose_print(gui, 'camera', 'Main: IOError: {}'.format(io_err))
    trigger.set_false('runProcess')
    Interface.choose_print(gui, 'camera', 'XimeaClientThread: Finished')

def process_worker(queue,process_values,trigger,gui=None):
    count = 0
    while trigger.get(name='runProcess'):
        while not queue.empty():
            pic = queue.get()
            Interface.choose_print(gui, 'process', 'pic {} hex: {}'.format(count,(hash(pic))))
            XimeaClient.save_image(pic,number=count)
            count += 1
    Interface.choose_print(gui, 'process', 'ProcessImageThread: Finished')

def start_threads(settings,gui=None):
    arduino_values = settings.get("Arduino")
    pic_queue = Queue.Queue(maxsize=0)
    trigger_master = ThreadTrigger()
    trigger_master.register('startArduino',False)
    trigger_master.register('startCamera', False)
    trigger_master.register('runProcess', True)
    trigger_master.register('runCamera', True)
    arduino = threading.Thread(name="ArduinoThread",target=arduino_worker,args=(arduino_values,settings.get("Main"),trigger_master),kwargs={'gui':gui})
    camera = threading.Thread(name="XimeaClientThread", target=camera_worker,args=(pic_queue,settings.get("XimeaClient"),arduino_values,trigger_master),kwargs={'gui':gui})
    process = threading.Thread(name="ProcessImageThread", target=process_worker,args=(pic_queue,settings.get("ProcessImage"),trigger_master),kwargs={'gui':gui})
    arduino.start()
    camera.start()
    process.start()

def main():
    settings = get_settings_dic(['Main','Arduino','XimeaClient','ProcessImage'])
    if(int(settings.get("Main")[0]) > 0):
        gui = Interface.ScarberryGui()
        gui.set_entry(settings)
        gui.start()
    else:
        start_threads(settings)

if __name__ == "__main__":
    main()

class ThreadTrigger:
    __trigger_dic = None
    def __init__(self):
        self.__trigger_dic = {}

    def register(self, name, state):
        self.__trigger_dic[name] = state

    def toggle(self, name):
        try:
            self.__trigger_dic[name] = not self.__trigger_dic[name]
        except KeyError as key_err:
            print key_err

    def set_true(self, name):
        try:
            self.__trigger_dic[name] = True
        except KeyError as key_err:
            print key_err

    def set_false(self, name):
        try:
            self.__trigger_dic[name] = False
        except KeyError as key_err:
            print key_err

    def get(self, name=''):
        try:
            if name != '':
                return self.__trigger_dic[name]
            else:
                return self.__trigger_dic
        except KeyError as key_err:
            print key_err
