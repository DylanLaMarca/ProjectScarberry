import struct
import numpy
import Interface
import math

class XimeaClient:
    pipe = None
    gui = None
    pipe_name = 'XimeaPipe'

    def __init__(self,framerate,gain,shrink,run_time,gui):
        self.gui = gui
        self.pipe = open(r'\\.\pipe\{}'.format(self.pipe_name), 'r+b', 0)
        exposure = (1000000/(int(framerate)))
        exposure -= math.pow(10,math.floor(math.log(exposure,10))-1)
        number_of_pics = (int(framerate))*((int(run_time))+1)
        Interface.choose_print(gui, 'camera', 'opening {}...'.format(r'\\.\pipe\{}'.format(self.pipe_name)))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(self.pipe_name, exposure))
        self.pipe.write(numpy.uint32(exposure))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(self.pipe_name, gain))
        self.pipe.write(numpy.uint32(gain))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(self.pipe_name, number_of_pics))
        self.pipe.write(numpy.uint32(number_of_pics))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(self.pipe_name, shrink))
        self.pipe.write(numpy.uint32(shrink))


    def get_image(self):
        image_length = struct.unpack('I', self.pipe.read(4))[0]
        print '----------{}'.format(image_length)
        pipe_input = self.pipe.read(image_length)
        self.pipe.seek(0)
        return pipe_input