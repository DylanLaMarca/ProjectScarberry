"""
Contains all of the code needed to control a XIMEA camera for ProjectScarberry
    :author: Dylan Michael LaMarca
    :contact: dylan@lamarca.org
    :GitHub: https://github.com/GhoulPoP/ProjectScarberry
    :Date: 7/2/2017 - 9/2/2017
"""
from ximea import xiapi
import Interface
import math

class XimeaCamera:
    gui = None
    cam = None
    img = None

    def __init__(self,framerate,gain=0,gui=None):
        self.gui = gui
        self.img = xiapi.Image()

        self.cam = xiapi.Camera()
        print('Opening camera...')
        self.cam.open_device()

        exposure = (1000000 / (int(framerate)))
        exposure -= math.pow(10, math.floor(math.log(exposure, 10)) - 1)
        self.cam.set_exposure(int(exposure))

        self.cam.set_gain(gain)

        self.cam.set_trigger_source('XI_TRG_EDGE_RISING')
        self.cam.set_gpi_mode('XI_GPI_TRIGGER')
        self.cam.set_gpo_selector('XI_GPO_PORT1')
        self.cam.set_gpo_mode('XI_GPO_FRAME_TRIGGER_WAIT')
        self.cam.set_imgdataformat('XI_MONO8')

    def start_aquisition(self):
        print('Starting data acquisition...')
        self.cam.start_acquisition()

    def stop_aquisition(self):
        print('Stopping acquisition...')
        self.cam.stop_acquisition()

    def close_camera(self):
        print('Closing camera...')
        self.cam.close_device()

    def get_image(self):
        self.cam.get_image(self.img)
        return self.img.get_image_data_numpy()
