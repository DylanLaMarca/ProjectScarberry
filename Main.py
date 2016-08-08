import XimeaClient
import struct

arduino_values = []
controller_values = []
process_values = []
with open('ScarberrySettings') as file:
    count = 0
    lines = file.readlines()
    for line in lines:
        if(line.startswith('Arduino')):
            arduino_values.append(line[line.index('[')+1:line.index(']')])
        if (line.startswith('XimeaController')):
            controller_values.append(line[line.index('[') + 1:line.index(']')])
        if (line.startswith('ProcessImage')):
            process_values.append(line[line.index('[') + 1:line.index(']')])

try:
    client = XimeaClient.XimeaClient(controller_values);
    count = 0
    run = True
    while run:
        try:
            current_image = client.get_image()
            client.save_image(current_image, count)
            count += 1
        except struct.error as struct_err:
            print('Server Disconnected: ({})'.format(struct_err))
            run = False
except IOError as io_err:
    print(io_err)
