import ArduinoController
import ProcessImage
import XimeaClient
import struct
import subprocess
import time
import Queue
import threading
import Interface

pic_queue = Queue.Queue(maxsize=0)
started_client = False
started_arduino = False
run_process_worker = True
run_camera_worker = True
main_values = None
arduino_values = None
camera_values = None
process_values = None
client = None
gui = None
run_time = 5
long_sleep = 6
sleep = 2

def format_settings():
    global main_values
    global arduino_values
    global camera_values
    global process_values
    settings = get_settings_dic(["Main","Arduino", "XimeaClient", "ProcessImage"])
    main_values = settings.get("Main")
    arduino_values = settings.get("Arduino")
    camera_values = settings.get("XimeaClient")
    process_values = settings.get("ProcessImage")

def get_settings_dic(keys):
    settings_dic = {}
    for key in keys:
        settings_dic[key] = []
    with open('ScarberrySettings') as file:
        print('Collecting {} information:'.format(file.name))
        for line in file.readlines():
            settings_dic[line[:line.index(':')]].append(line[line.index('[') + 1:line.index(']')])
        print settings_dic
    return settings_dic


def arduino_worker():
    global arduino_values
    global started_arduino
    global started_client
    controller = ArduinoController.ArduinoController(6,gui)
    for value in arduino_values:
        controller.write_value(value, sleep)

    started_arduino = True
    while not started_client:
        pass
    controller.write_value(1,0)
    time.sleep(run_time)
    controller.write_value(4,0)
    Interface.chose_print(gui, 'arduino', 'ArduinoThread: Finished')


def camera_worker():
    global client
    global pic_queue
    global camera_values
    global started_client
    global run_process_worker
    global started_arduino
    subprocess.Popen('XimeaController\\XimeaController\\bin\\Debug\\XimeaController.exe')
    time.sleep(long_sleep)
    try:
        client = XimeaClient.XimeaClient(camera_values,gui);
        run = True
        started_client = True
        while not started_arduino:
            pass
        while run:
            try:
                current_image = client.get_image()
                pic_queue.put(current_image)
            except struct.error as struct_err:
                Interface.chose_print(gui,'camera','Main: Server Disconnected: struct_err: {}'.format(struct_err))
                run = False
    except IOError as io_err:
        Interface.chose_print(gui, 'camera','Main: IOError: {}'.format(io_err))
    run_process_worker = False
    Interface.chose_print(gui, 'camera','XimeaClientThread: Finished')


def process_worker():
    global pic_queue
    global process_values
    count = 0
    while run_process_worker:
        while not pic_queue.empty():
            pic = pic_queue.get()
            Interface.chose_print(gui, 'process','pic hex: {}'.format((hash(pic))))
            client.save_image(pic,count)
            count += 1
    Interface.chose_print(gui, 'process', 'ProcessImageThread: Finished')

def start_threads():
    arduino = threading.Thread(name="ArduinoThread", target=arduino_worker)
    camera = threading.Thread(name="XimeaClientThread", target=camera_worker)
    process = threading.Thread(name="ProcessImageThread", target=process_worker)
    arduino.start()
    camera.start()
    process.start()

def main():
    global gui
    format_settings()
    if(int(main_values[0]) > 0):
        gui = Interface.ScarberryGui(start_button_function=start_threads)
        gui.start()
    else:
        start_threads()

if __name__ == "__main__":
    main()
