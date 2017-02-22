"""
Contains all of the code needed to control a XIMEA camera for ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dylan@lamarca.org
    :GitHub: https://github.com/GhoulPoP/ProjectScarberry
    :Date: 7/2/2017 - 21/2/2017
"""
from ximea import xiapi
import Interface
import Main
import math

class XimeaCamera:
    """
     An object used to establish and manage a connection to capture images with a Ximea Camera.
         :ivar camera: The Ximea camera controlled by ProjectScarberry.
         :type camera: xiapi.Camera
         :ivar image: Object used to temporarily store the most recently captured picture.
         :type image: xiapi.Image
         :ivar gui: Optional interface used to print.
         :type gui: Interface.ScarberryGui
         :function start_acquisition: Starts acquisition of the Ximea camera.
         :function stop_acquisition: Stops aquisition of the Ximea camera.
         :function close_camera: Closes all communication with the Ximea camera.
         :function get_image: Prompts the Ximea camera to capture a photo after the next GPI spike.
     """
    camera = None
    image = None
    gui = None

    def __init__(self,framerate,gain=0,gui=None):
        """
        Initializes an instance of XimeaCamera.
            :argument framerate: Number of pictures taken a second.
            :type framerate: int
            :keyword gain: Brightness modifier of pictures taken.
            type gain: int, float [0 to 6](default 0)
            :keyword gui: Optional interface used to print(default None).
            :type gui: Interface.ScarberryGui
        """
        self.gui = gui
        self.image = xiapi.Image()

        self.camera = xiapi.Camera()
        Interface.choose_print(gui, 'camera', 'Opening camera...')
        try:
            self.camera.open_device()

            exposure = (1000000 / (int(framerate)))
            exposure -= math.pow(10, math.floor(math.log(exposure, 10)) - 1)
            self.camera.set_exposure(int(exposure))

            if gain < 0:
                gain = 0
            if gain > 6:
                gain = 6
            self.camera.set_gain(float(gain))

            self.camera.set_trigger_source('XI_TRG_EDGE_RISING')
            self.camera.set_gpi_mode('XI_GPI_TRIGGER')
            self.camera.set_gpo_selector('XI_GPO_PORT1')
            self.camera.set_gpo_mode('XI_GPO_FRAME_TRIGGER_WAIT')
            self.camera.set_imgdataformat('XI_MONO8')
        except xiapi.Xi_error:
            Interface.choose_print(gui, 'camera', 'Xi_error: ERROR 56: No Devices Found')
            Main.abort_session()

    def start_acquisition(self):
        """
        Starts acquisition of the Ximea camera.
        """
        Interface.choose_print(self.gui,'camera','Starting data acquisition...')
        self.camera.start_acquisition()

    def stop_acquisition(self):
        """
        Stops aquisition of the Ximea camera.
        """
        Interface.choose_print(self.gui, 'camera','Stopping acquisition...')
        self.camera.stop_acquisition()

    def close_camera(self):
        """
        Closes all communication with the Ximea camera.
        """
        Interface.choose_print(self.gui, 'camera','Closing camera...')
        self.camera.close_device()

    def get_image(self):
        """
        Prompts the Ximea camera to capture a photo after the next GPI spike.
        """
        try:
            self.camera.get_image(self.image)
            return self.image.get_image_data_numpy()
        except xiapi.Xi_error:
            Interface.choose_print(self.gui, 'camera', 'Xi_error: ERROR 10: Timeout')
            Main.abort_session()
            return None
