import ArduinoController
import ProcessImage
import XimeaClient
import struct
import subprocess
import time
import Queue
import threading
import cv2

pic_queue = Queue.Queue(maxsize=0)
started_client = False
started_arduino = False
run_process_worker = True;
run_camera_worker = True;
arduino_values = None
camera_values = None
process_values = None
client = None
run_time = 20
long_sleep = 6
sleep = 2

def format_settings():
    global arduino_values
    global camera_values
    global process_values
    settings = get_settings_dic(["Arduino", "XimeaClient", "ProcessImage"])
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
    controller = ArduinoController.ArduinoController(6)
    for value in arduino_values:
        controller.write_value(value, sleep)

    started_arduino = True
    while not started_client:
        pass
    controller.write_value(1,0)
    time.sleep(run_time)
    controller.write_value(4,0)
    print 'ArduinoThread: Finished'

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
        client = XimeaClient.XimeaClient(camera_values);
        run = True
        started_client = True
        while not started_arduino:
            pass
        while run:
            try:
                current_image = client.get_image()
                pic_queue.put(current_image)
            except struct.error as struct_err:
                print('Main: Server Disconnected: struct_err: {}'.format(struct_err))
                run = False
    except IOError as io_err:
        print('Main: IOError: {}'.format(io_err))
    run_process_worker = False
    print 'XimeaClientThread: Finished'

def process_worker():
    global pic_queue
    global process_values
    count = 0
    while run_process_worker:
        while not pic_queue.empty():
            pic = pic_queue.get()
            print(hash(pic))
            client.save_image(pic,count)
            count += 1
    print 'ProcessImageThread: Finished'

format_settings()
arduino = threading.Thread(name="ArduinoThread",target=arduino_worker)
camera = threading.Thread(name="XimeaClientThread",target=camera_worker)
process = threading.Thread(name="ProcessImageThread",target=process_worker)

arduino.start()
camera.start()
process.start()
