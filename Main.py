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
pic_queue = Queue.Queue(maxsize=0)
started_client = False
started_arduino = False
run_process_worker = True
run_camera_worker = True
main_values = None
arduino_values = None
camera_values = None
process_values = None
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
    with open(settings_file_directory) as file:
        print('Collecting {} information:'.format(file.name))
        for line in file.readlines():
            settings_dic[line[:line.index(':')]].append(line[line.index('[') + 1:line.index(']')])
        print settings_dic
    return settings_dic

def set_values(new_main_values,new_arduino_values,new_camera_values,new_process_values):
    global main_values
    global arduino_values
    global camera_values
    global process_values
    main_values = new_main_values
    arduino_values = new_arduino_values
    camera_values = new_camera_values
    process_values = new_process_values

def save_settings():
    filename = settings_file_directory
    file = open(filename, 'w')
    file.truncate()
    file.write(format_values_to_save("Main",main_values))
    file.write(format_values_to_save("Arduino", arduino_values))
    file.write(format_values_to_save("XimeaClient", camera_values))
    file.write(format_values_to_save("ProcessImage", process_values))
    file.close()

def format_values_to_save(key,values):
    output = ""
    for value in values:
        output += '{}:[{}]\n'.format(key,value)
        print output
    return output

def arduino_worker(gui):
    global arduino_values
    global started_arduino
    global started_client
    controller = ArduinoController.ArduinoController(arduino_values[0], gui)
    for count in range(len(arduino_values)-1):
        controller.write_value(arduino_values[count+1], sleep)

    started_arduino = True
    while not started_client:
        pass
    controller.write_value(1,0)
    time.sleep(float(main_values[1]))
    controller.write_value(4,0)
    Interface.choose_print(gui, 'arduino', 'ArduinoThread: Finished')

def camera_worker(gui):
    global client
    global pic_queue
    global camera_values
    global started_client
    global run_process_worker
    global started_arduino
    subprocess.Popen('XimeaController\\XimeaController\\bin\\Debug\\XimeaController.exe')
    time.sleep(long_sleep)
    try:
        camera_values.append((1000000/camera_values[0])-100)
        client = XimeaClient.XimeaClient(camera_values, gui);
        run = True
        started_client = True
        while not started_arduino:
            pass
        while run:
            try:
                current_image = client.get_image()
                pic_queue.put(current_image)
            except struct.error as struct_err:
                Interface.choose_print(gui, 'camera', 'Main: Server Disconnected: struct_err: {}'.format(struct_err))
                run = False
    except IOError as io_err:
        Interface.choose_print(gui, 'camera', 'Main: IOError: {}'.format(io_err))
    run_process_worker = False
    Interface.choose_print(gui, 'camera', 'XimeaClientThread: Finished')

def process_worker(gui):
    global pic_queue
    global process_values
    count = 0
    while run_process_worker:
        while not pic_queue.empty():
            pic = pic_queue.get()
            Interface.choose_print(gui, 'process', 'pic {} hex: {}'.format(count,(hash(pic))))
            client.save_image(pic,count)
            count += 1
    Interface.choose_print(gui, 'process', 'ProcessImageThread: Finished')

def start_threads(gui):
    arduino = threading.Thread(name="ArduinoThread",target=arduino_worker,args=(gui,))
    camera = threading.Thread(name="XimeaClientThread", target=camera_worker,args=(gui,))
    process = threading.Thread(name="ProcessImageThread", target=process_worker,args=(gui,))
    arduino.start()
    camera.start()
    process.start()

def main():
    gui = None
    format_settings()
    if(int(main_values[0]) > 0):
        gui = Interface.ScarberryGui()
        gui.set_entry()
        gui.start()
    else:
        start_threads(gui)

if __name__ == "__main__":
    main()
