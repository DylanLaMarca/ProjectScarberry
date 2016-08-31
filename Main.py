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

def get_settings_dict(keys):
    settings_dic = {}
    for key in keys:
        settings_dic[key] = {}
    with open(settings_file_directory) as file:
        print('Collecting {} information:'.format(file.name))
        for line in file.readlines():
            sub_dict = line[:line.index(':')]
            sub_key = line[line.index(':') + 1:line.index('[')]
            value = line[line.index('[') + 1:line.index(']')]
            settings_dic[sub_dict][sub_key] = value
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

def format_values_to_save(key,dict):
    output = ""
    sub_keys = dict.keys()
    for sub_key in sub_keys:
        output += '{}:{}[{}]\n'.format(key,sub_key,dict.get(sub_key))
        print output
    return output

def arduino_worker(arduino_values,main_values,trigger,gui=None):
    controller = ArduinoController.ArduinoController(arduino_values.get("SerialPort"), gui)
    controller.write_value(arduino_values.get("FrameRate"), 2)
    controller.write_value(arduino_values.get("StrobeCount"), 2)
    controller.write_value(arduino_values.get("DutyCycle"), 2)
    while not trigger.get(name='startArduino'):
        pass
    controller.write_value(1,0)
    trigger.set_true('startCamera')
    time.sleep(float(main_values.get("RunTime"))+1)
    controller.write_value(4,0)
    Interface.choose_print(gui, 'arduino', 'ArduinoThread: Finished')

def camera_worker(queue,camera_values,arduino_values,main_values,trigger,gui=None):
    subprocess.Popen('XimeaController\\XimeaController\\bin\\Debug\\XimeaController.exe')
    time.sleep(6)
    try:
        client = XimeaClient.XimeaClient(arduino_values.get("FrameRate"),
                                         camera_values.get("Gain"),
                                         camera_values.get("ShrinkQuotient"),
                                         main_values.get("RunTime"),
                                         gui);
        run = True
        time.sleep(10)
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
    pic_count = 0
    while trigger.get(name='runProcess'):
        while not queue.empty():
            pic = queue.get()
            Interface.choose_print(gui, 'process', 'pic {} hex: {}'.format(pic_count,(hash(pic))))
            opencv_pic = ProcessImage.convert_to_cv(pic)
            formated_number = ProcessImage.format_number(pic_count,int(process_values.get("NumberPadding")))
            ProcessImage.save_image(opencv_pic,
                                    formated_number,
                                    image_direcoty=process_values.get("ImageDirectory"),
                                    name=process_values.get("BaseName"),
                                    extention=process_values.get("FileExtension"))
            data_filename = '{}\\data\\data-{}_{}{}'.format(process_values.get("ImageDirectory"),
                                                            process_values.get("BaseName"),
                                                            formated_number,
                                                            '.txt')
            if process_values.get("SaveDraw"):
                ProcessImage.draw_and_data(opencv_pic,
                                  '{}\\data\\data-{}_{}{}'.format(process_values.get("ImageDirectory"),
                                                                  process_values.get("BaseName"),
                                                                  formated_number,
                                                                  process_values.get("FileExtension")),
                                  data_filename,
                                process_values.get("BlurValue"),
                                process_values.get("ThreshLimit"),
                                draw_rois=process_values.get("DrawROIs"),
                                draw_centroid=process_values.get("DrawCentroid"),
                                draw_vectors=process_values.get("DrawVector"),
                                draw_count=process_values.get("DrawCount"))
            else:
                data = ProcessImage.get_data(opencv_pic,
                                      process_values.get("BlurValue"),
                                      process_values.get("ThreshLimit"))
                ProcessImage.save_data(data,data_filename)
            pic_count += 1
    Interface.choose_print(gui, 'process', 'ProcessImageThread: Finished')

def start_threads(settings,gui=None):
    arduino_values = settings.get("Arduino")
    main_values = settings.get("Main")
    pic_queue = Queue.Queue(maxsize=0)
    trigger_master = ThreadTrigger()
    trigger_master.register('startArduino',False)
    trigger_master.register('startCamera', False)
    trigger_master.register('runProcess', True)
    trigger_master.register('runCamera', True)
    arduino = threading.Thread(name="ArduinoThread",
                               target=arduino_worker,
                               args=(arduino_values,
                                     main_values,
                                     trigger_master),
                               kwargs={'gui':gui})
    camera = threading.Thread(name="XimeaClientThread",
                              target=camera_worker,
                              args=(pic_queue,settings.get("XimeaClient"),
                                    arduino_values,
                                    main_values,
                                    trigger_master),
                              kwargs={'gui':gui})
    process = threading.Thread(name="ProcessImageThread",
                               target=process_worker,
                               args=(pic_queue,
                                     settings.get("ProcessImage"),
                                     trigger_master),
                               kwargs={'gui':gui})
    arduino.start()
    camera.start()
    process.start()

def main():
    settings = get_settings_dict(['Main','Arduino','XimeaClient','ProcessImage'])
    if(int(settings.get("Main").get("UseInterface")) > 0):
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
