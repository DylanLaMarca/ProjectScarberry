"""
Contains all of the code needed to interact and utilize the C# program XimeaController for ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dlamarca@u.washington.edu
    :Date: 26/7/2016 - 2/9/2016
    :class XimeaClient: An object used to establish and manage a pipe with the C# program XimeaController to receive images.
"""
import struct
import numpy
import Interface
import math

class XimeaClient:
    """
    An object used to establish and manage a pipe with the C# program XimeaController to receive images.
        :cvar PIPE_NAME: The name of the pipe created by XimeaController
        :type PIPE_NAME: string
        :ivar pipe: The pipe used to receive and send information from XimeaController.
        :type pipe: file
        :ivar gui: Optional interface used to print.
        :type gui: Interface.ScarberryGui
        :function get_image: Waits for the pipe to send a picture, receives it, and unpacks it.
    """
    PIPE_NAME = 'XimeaPipe'
    pipe = None
    gui = None

    def __init__(self,framerate,gain,shrink,run_time,gui=None):
        """
        Initializes an instance of XimeaClient
            :argument framerate: Number of pictures being taken a second.
            :type framerate: int
            :argument gain: Light sensitivity in decibels.
            :type gain: int (between 0 and 6)
            :argument shrink: By what factor the pictures size will be decreased by.
            :type shrink: int (must be 1,2,or a multiple of 4)
            :argument run_time: Amount of time in seconds the camera will be actively taking pictures.
            :type runtime: int, float
            :keyword gui: Optional interface used to print(default None).
            :type gui: Interface.ScarberryGui
        """
        self.gui = gui
        self.pipe = open(r'\\.\pipe\{}'.format(XimeaClient.PIPE_NAME), 'r+b', 0)
        exposure = (1000000/(int(framerate)))
        exposure -= math.pow(10,math.floor(math.log(exposure,10))-1)
        number_of_pics = (int(framerate))*((int(run_time))+1)
        Interface.choose_print(gui, 'camera', 'opening {}...'.format(r'\\.\pipe\{}'.format(XimeaClient.PIPE_NAME)))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(XimeaClient.PIPE_NAME, exposure))
        self.pipe.write(numpy.uint32(exposure))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(XimeaClient.PIPE_NAME, gain))
        self.pipe.write(numpy.uint32(gain))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(XimeaClient.PIPE_NAME, number_of_pics))
        self.pipe.write(numpy.uint32(number_of_pics))
        Interface.choose_print(gui, 'camera', 'sending {} {}'.format(XimeaClient.PIPE_NAME, shrink))
        self.pipe.write(numpy.uint32(shrink))

    def get_image(self):
        """
        Wait for the pipe to send a picture, receive it, and unpack it.
            :return: A packed picture sent from XimeaController
            :rtype: base64 string
        """
        image_length = struct.unpack('I', self.pipe.read(4))[0]
        print '----------{}'.format(image_length)
        pipe_input = self.pipe.read(image_length)
        self.pipe.seek(0)
        return pipe_input
