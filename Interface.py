"""
Contains all of the code used to display and edit program parameters, outside of the ScarberrySettings file and the Python Shell, for ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dylan@lamarca.org
    :GitHub: https://github.com/GhoulPoP/ProjectScarberry
    :Date: 15/8/2016 - 21/2/2017
    :class ScarberryGui: An object used to display the string output of the threads in main as well as displaying and manipulating the values stored in ScarberrySettings and used in Main.
    :function choose_print: Evaluates whether or not text shoud be printed to the Python Shell or an interface.
"""
from Tix import Tk
from Tkinter import *
import tkFileDialog
import ttk
import Main
import subprocess
import os

class ScarberryGui:
    """
    An object used to display the string output of the threads in main as well as displaying and manipulating the values stored in ScarberrySettings and used in Main.
        :ivar master: The master frame which all elements, including content, are added to.
        :type master: instance
        :ivar content: The frame which all elements are displayed in a grid upon.
        :type content: Frame
        :ivar image_directory:A string used to store and manipulate 'ProcessImage:ImageDirectory' in ScarberrySettings.
        :type image_directory: string
        :ivar com: An EntryElement used to store and manipulate 'Arduino:SerialPort' in ScarberrySettings.
        :type com: EntryElement
        :ivar runtime: An EntryElement used to store and manipulate 'Main:RunTime' in ScarberrySettings.
        :type runtime: EntryElement
        :ivar framerate: An EntryElement used to store and manipulate 'Main:RunTime' in ScarberrySettings.
        :type framerate: EntryElement
        :ivar strobecount: An EntryElement used to store and manipulate 'Arduino:StrobeCount' in ScarberrySettings.
        :type strobecount: EntryElement
        :ivar dutycycle: An EntryElement used to store and manipulate 'Arduino:DutyCycle' in ScarberrySettings.
        :type dutycycle: EntryElement
        :ivar thresh: An EntryElement used to store and manipulate 'ProcessImage:ThreshLimit' in ScarberrySettings.
        :type thresh: EntryElement
        :ivar name: An EntryElement used to store and manipulate 'ProcessImage:BaseName' in ScarberrySettings.
        :type name: EntryElement
        :ivar padding: An EntryElement used to store and manipulate 'ProcessImage:NumberPadding' in ScarberrySettings.
        :type padding: EntryElement
        :ivar extension: An OptionMenuElement used to store and manipulate 'ProcessImage:FileExtension' in ScarberrySettings.
        :type extension: OptionMenuElement
        :ivar blur: An OptionMenuElement used to store and manipulate 'ProcessImage:BlurValue' in ScarberrySettings.
        :type blur: OptionMenuElement
        :ivar gain: An OptionMenuElement used to store and manipulate 'XimeaController:Gain' in ScarberrySettings.
        :type gain: OptionMenuElement
        :ivar shrink: An OptionMenuElement used to store and manipulate 'XimeaController:ShrinkQuotient' in ScarberrySettings.
        :type shrink: OptionMenuElement
        :ivar draw: An CheckBoxElement used to store and manipulate 'ProcessImage:SaveDraw' in ScarberrySettings.
        :type draw: CheckBoxElement
        :ivar draw_roi: An CheckBoxElement used to store and manipulate 'ProcessImage:DrawROIs' in ScarberrySettings.
        :type draw_roi: CheckBoxElement
        :ivar draw_centroid: An CheckBoxElement used to store and manipulate 'ProcessImage:DrawCentroid' in ScarberrySettings.
        :type draw_centroid: CheckBoxElement
        :ivar draw_colour: An CheckBoxElement used to store and manipulate 'ProcessImage:DrawColour' in ScarberrySettings.
        :type draw_colour: CheckBoxElement
        :ivar draw_count: An CheckBoxElement used to store and manipulate 'ProcessImage:DrawCount' in ScarberrySettings.
        :type draw_count: CheckBoxElement
        :ivar arduino_controller_text: A TextElement used to display the string output of Main's ArduinoThread.
        :type arduino_controller_text: TextElement
        :ivar ximea_controller_text: A TextElement used to display the string output of Main's XimeaControllerThread.
        :type ximea_controller_text: TextElement
        :ivar save_image_text: A TextElement used to display the string output of Main's SaveImageThread.
        :type save_image_text: TextElement
        :ivar data_image_text: A TextElement used to display the string output of Main's DataImageThread.
        :type data_image_text: TextElement
        :ivar option_elements: A list used to efficiently add all of the EntryElements and OptionMenuElement to content.
        :type option_elements: list
        :ivar text_elements: A list used to efficiently add all of the TextElements to content.
        :type text_elements: list
        :class EntryElement: An object used to store and manipulate a variable, a Label element, and an Entry element all as one unit on ScarberryGui.
        :class OptionMenuElement: An object used to store and manipulate a variable, a Label element, and an OptionMenu element all as one unit on ScarberryGui.
        :class CheckBoxElement: An object used to store and manipulate a variable and a Checkbutton element on ScarberryGui.
        :class TextElement: An object used to store and manipulate a LabelFrame and Text element as one unit on ScarberryGui.
        :function format_menu: Formats the top-menu in ScarberryGui.
        :function format_entries: Formats the text entry bars in ScarberryGui.
        :function format_optionmenus: Formats the dropdown choice menus in ScarberryGui.
        :function generate_optionmenu_values: Creates a list of number values from a simple loop to be stored as the values of a dropdown choice menu.
        :function format_text: Formats the text fields in ScarberryGui.
        :function start: Opens ScarberryGui and begins its main loop.
        :function set_directory: Sets self.image_directory by creating a miniaturized, pre-built file explorer.
        :function open_settings: Opens ScarberrySettings in notepad.exe.
        :function open_images: Opens the current image directory using windows explorer.
        :function open_data: Opens the current data directory using windows explorerand creates a new data directory if it does not exist.
        :function reset_to_preset: Sets all of the input elements to their corresponding values stored in ScarberrySettings.
        :function set_input: Sets all of the input elements to their corresponding values stored in a dictionary.
        :function get_input_values_dict: Creates a dictionary of dictionaries containing all of the values stored in the input elements on the current instance of ScargerryGui.
        :function set_presets: Sets the values stored in ScarberrySettings to their corresponding values stored in the current instance of ScarberryGui.
    """
    master = None
    content = None
    image_directory = ''
    com = None
    runtime = None
    framerate = None
    strobecount = None
    dutycycle = None
    thresh = None
    name = None
    padding = None
    extension = None
    blur = None
    gain = None
    shink = None
    draw = None
    draw_roi = None
    draw_centroid = None
    draw_colour = None
    draw_count = None
    arduino_controller_text = None
    ximea_controller_text = None
    save_image_text = None
    data_image_text = None
    option_elements = []
    text_elements = []

    def __init__(self):
        """
        Initializes an instance of ScarberryGui
        """
        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.wm_title('Project Scarberry')
        self.master.wm_iconbitmap('icon\\butterflybrown-256.ico')
        self.content = ttk.Frame(self.master)
        frame = ttk.Frame(self.content, borderwidth=2, relief='sunken')
        extender = Label(self.content, text='                                              ')

        self.format_menu()
        self.format_entries()
        self.format_optionmenus()
        directory_button = Button(self.content,
                                  text='   Set Pic Directory   ',
                                  command=self.set_directory)
        directory_button.pack()
        start_button = Button(self.content,
                              text='   Start   ',
                              command=lambda:Main.start_threads(self.get_input_values_dict(), gui=self))
        start_button.pack()
        abort_button = Button(self.content,
                              text='   Abort   ',
                              command=lambda:Main.abort_session())
        abort_button.pack()
        self.format_texts()

        self.content.grid(column=0, row=0)
        columns = 6
        rows = 20
        frame.grid(column=0, row=0, columnspan=columns, rowspan=rows)
        extender.grid(column=0, row=0,sticky=W)
        list_count = 0
        for option in self.option_elements:
            option.grid(list_count,0)
            list_count+=1

        self.draw = ScarberryGui.CheckBoxElement(self.content,"Draw: ",5,W)
        self.draw.grid(list_count,0)
        self.draw_colour = ScarberryGui.CheckBoxElement(self.content,"In Colour ",20,W)
        self.draw_colour.grid(list_count+1,0)
        self.draw_roi = ScarberryGui.CheckBoxElement(self.content,"Roi ",2,E)
        self.draw_roi.grid(list_count+1,0)
        self.draw_centroid = ScarberryGui.CheckBoxElement(self.content,"Centroid ",20,W)
        self.draw_centroid.grid(list_count+2,0)
        self.draw_count = ScarberryGui.CheckBoxElement(self.content, "Count ",2,E)
        self.draw_count.grid(list_count+2,0)

        directory_button.grid(column=0, row=list_count+3, padx=5)
        start_button.grid(column=0, row=list_count+4, sticky=W, padx=5)
        abort_button.grid(column=0, row=list_count+4, sticky=E, padx=5)

        count = 0
        for text in self.text_elements:
            text.grid(1+((columns/3)*count),rows)
            count += 1

    def format_menu(self):
        """
        Formats the top-menu in ScarberryGui.
        """
        menu_bar = Menu(self.master, tearoff=0)
        self.master.config(menu=menu_bar)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label='Open Images',command=self.open_images)
        file_menu.add_command(label='Open Data',command=self.open_data)
        file_menu.add_command(label='Exit')
        menu_bar.add_cascade(label='File', menu=file_menu)
        settings_menu = Menu(menu_bar)
        preset_menu = Menu(settings_menu)
        preset_menu.add_command(label='Open Presets', command=self.open_settings)
        preset_menu.add_command(label='Set Presets', command=self.set_presets)
        preset_menu.add_command(label='Reset to Presets', command=self.reset_to_preset)
        settings_menu.add_cascade(label='Presets', menu=preset_menu, underline=0)
        menu_bar.add_cascade(label='Settings', menu=settings_menu)
        menu_bar.add_command(label='About')

    def format_entries(self):
        """
        Formats the text entry bars in ScarberryGui.
        """
        self.com = ScarberryGui.EntryElement(self.content,'Serial Port:            COM',2)
        self.runtime = ScarberryGui.EntryElement(self.content,'RunTime:  ',5)
        self.framerate = ScarberryGui.EntryElement(self.content,'Framerate:  ',5)
        self.strobecount = ScarberryGui.EntryElement(self.content,'Strobe Count:  ',5)
        self.dutycycle = ScarberryGui.EntryElement(self.content,'Duty Cycle:                0.',2)
        self.thresh = ScarberryGui.EntryElement(self.content,'Thresh Limit:  ',5)
        self.name = ScarberryGui.EntryElement(self.content,'Pic Name:  ',12)
        self.padding = ScarberryGui.EntryElement(self.content,'Num Padding: ',3)
        self.option_elements.extend([self.com,
                                     self.runtime,
                                     self.framerate,
                                     self.strobecount,
                                     self.dutycycle,
                                     self.thresh,
                                     self.name,
                                     self.padding])

    def format_optionmenus(self):
        """
        Formats the dropdown choice menus in ScarberryGui.
        """
        self.extension = ScarberryGui.OptionMenuElement(self.content,self.master,'Pic Extension: ',['.TIF','.png','.jpg','.gif'])
        self.blur = ScarberryGui.OptionMenuElement(self.content, self.master,'Blur Val: ', self.generate_optionmenu_values(15, 3, 2))
        self.gain = ScarberryGui.OptionMenuElement(self.content, self.master,'Gain Val:  ', self.generate_optionmenu_values(7, 0, 1))
        self.shrink = ScarberryGui.OptionMenuElement(self.content,self.master,'Shrink Val:  ',['1','2','4','8','16','32'])
        self.option_elements.extend([self.extension,
                                     self.blur,
                                     self.gain,
                                     self.shrink])

    def generate_optionmenu_values(self, number, start, increment):
        """
        Creates a list of number values from a simple loop to be stored as the values of a dropdown choice menu.
            :argument number: The number of values that will be in the returned list.
            :type number: int
            :argument start:
            :type start: int, float
            :argument increment:
            :type increment: int, float
            :return: A list of values
            :rtype: list
        """
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu

    def format_texts(self):
        """
        Formats the text fields in ScarberryGui.
        """
        text_height = 25
        text_width = 20
        self.arduino_controller_text = ScarberryGui.TextElement(self.content,'ArduinoController',text_height,text_width)
        self.ximea_controller_text = ScarberryGui.TextElement(self.content,'XimeaController',text_height,text_width)
        self.save_image_text = ScarberryGui.TextElement(self.content, 'SaveImage', text_height, text_width)
        self.data_image_text = ScarberryGui.TextElement(self.content, 'DataImage', text_height, text_width)
        self.text_elements = [self.arduino_controller_text,
                              self.ximea_controller_text,
                              self.save_image_text,
                              self.data_image_text]

    def start(self):
        """
        Opens ScarberryGui and begins its main loop.
        """
        self.master.mainloop()

    def set_directory(self):
        """
        Sets self.image_directory by creating a miniaturized, pre-built file explorer.
        """
        self.image_directory = tkFileDialog.askdirectory()

    def open_settings(self):
        """
        Opens ScarberrySettings in notepad.exe.
        """
        subprocess.Popen(["notepad.exe", Main.SETTINGS_FILE_DIRECTORY])

    def open_images(self):
        """
        Opens the current image directory using windows explorer.
        """
        subprocess.Popen(["explorer.exe", "{}".format(self.image_directory.replace('/','\\'))])

    def open_data(self):
        """
        Opens the current data directory using windows explorerand creates a new data directory if it does not exist.
        """
        print self.image_directory + '/data'
        data_directory = "{}\\data".format(self.image_directory.replace('/','\\'))
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        subprocess.Popen(["explorer.exe", data_directory])

    def reset_to_preset(self):
        """
        Sets all of the input elements to their corresponding values stored in ScarberrySettings.
        """
        self.set_inputs(Main.get_settings_dict(['Main', 'Arduino', 'XimeaController', 'ProcessImage']))

    def set_inputs(self, settings):
        """
         Sets all of the input elements to their corresponding values stored in a dictionary.
            :argument settings: All of the values which will replace the current values in the input elements on ScarberryGui.
            :type settings: dict
        """
        main_values = settings.get("Main")
        arduino_values = settings.get("Arduino")
        camera_values = settings.get("XimeaController")
        process_values = settings.get("ProcessImage")
        self.image_directory = process_values.get("ImageDirectory")
        self.com.set_text(arduino_values.get("SerialPort"))
        self.runtime.set_text(main_values.get("RunTime"))
        self.framerate.set_text(arduino_values.get("FrameRate"))
        self.strobecount.set_text(arduino_values.get("StrobeCount"))
        raw_dutycycle = arduino_values.get("DutyCycle")
        self.dutycycle.set_text((raw_dutycycle)[raw_dutycycle.index('.')+1:])
        self.thresh.set_text(process_values.get("ThreshLimit"))
        self.name.set_text(process_values.get("BaseName"))
        self.padding.set_text(process_values.get("NumberPadding"))
        self.extension.set_option(process_values.get("FileExtension"))
        self.blur.set_option(process_values.get("BlurValue"))
        self.gain.set_option(camera_values.get("Gain"))
        self.shrink.set_option(camera_values.get("ShrinkQuotient"))
        self.draw.value.set(process_values.get("SaveDraw"))
        self.draw_roi.value.set(process_values.get("DrawROIs"))
        self.draw_centroid.value.set(process_values.get("DrawCentroid"))
        self.draw_colour.value.set(process_values.get("DrawColour"))
        self.draw_count.value.set(process_values.get("DrawCount"))

    def get_input_values_dict(self):
        """
        Creates a dictionary of dictionaries containing all of the values stored in the input elements on the current instance of ScargerryGui.
            :return: A dictionary of dictionaries containing all of the values stored in the input elements.
            :rtype: dict
        """
        new_main_values = {"UseInterface":1,
                           "RunTime":self.runtime.value.get()}
        new_arduino_values = {"SerialPort":self.com.value.get(),
                              "FrameRate":self.framerate.value.get(),
                              "StrobeCount":self.strobecount.value.get(),
                              "DutyCycle":float('.' + self.dutycycle.value.get())}
        new_camera_values = {"Gain":self.gain.value.get(),
                             "ShrinkQuotient":self.shrink.value.get()}
        new_process_values = {"BlurValue":self.blur.value.get(),
                              "ThreshLimit":self.thresh.value.get(),
                              "ImageDirectory":self.image_directory,
                              "BaseName":self.name.value.get(),
                              "NumberPadding":self.padding.value.get(),
                              "FileExtension":self.extension.value.get(),
                              "SaveDraw":self.draw.value.get(),
                              "DrawROIs":self.draw_roi.value.get(),
                              "DrawCentroid":self.draw_centroid.value.get(),
                              "DrawColour":self.draw_colour.value.get(),
                              "DrawCount":self.draw_count.value.get()}
        return {'Main':new_main_values,
                'Arduino':new_arduino_values,
                'XimeaController':new_camera_values,
                'ProcessImage':new_process_values}

    def set_presets(self):
        """
        Sets the values stored in ScarberrySettings to their corresponding values stored in the current instance of ScarberryGui.
        """
        Main.save_settings(self.get_input_values_dict())

    class EntryElement:
        """
        An object used to store and manipulate a variable, a Label element, and an Entry element all as one unit on ScarberryGui.
            :ivar value: The value stored in Entry.
            :type value: string
            :ivar label: The text displayed to the left of the Entry element identifying its purpose.
            :type label: Label
            :ivar entry: The Entry element used to input text and change the content of value.
            :type entry: Entry
            :function grid: Sets the location of the Label and Entry elements on content.
            :function set_text: Replaces the text of the Entry element with a new string.
        """
        value = None
        label = None
        entry = None
        def __init__(self,content,title,width):
            """
            Initializes an instance of EntryElement.
                :argument content: The Frame which the Label and Entry elements will be displayed upon.
                :type content: Frame
                :argument title: The text stored in the Label element next to the Entry element.
                :type title: string
                :argument width: The number of characters wide the Entry element will be.
                :type width: int
            """
            self.value = StringVar()
            self.label = Label(content, text=title)
            self.entry = Entry(content, width=width, textvariable=self.value)
        def grid(self,row,column):
            """
            Sets the location of the Label and Entry elements on content.
                :argument row: The row (y axis) which the Label and Entry elements will be put at.
                :type row: int
                :argument column: The column (x axis) which the Label and Entry elements will be put at.
                :type column: int
            """
            self.label.grid(column=column, row=row, sticky=W, padx=5)
            self.entry.grid(column=column, row=row, sticky=E, padx=5)
        def set_text(self,text):
            """
            Replaces the text of the Entry element with a new string.
                :argument text: The new replacement text.
                :type text: string, int, float
            """
            self.entry.delete(0, END)
            self.entry.insert(0, text)

    class OptionMenuElement:
        """
        An object used to store and manipulate a variable, a Label element, and an OptionMenu element all as one unit on ScarberryGui.
            :ivar content: The Frame which the Label and OptionMenu elements will be displayed upon.
            :type content: Frame
            :ivar label: The text displayed to the left of the optionMenu element identifying its purpose.
            :type label: Label
            :ivar options: The list of values stored as choosable options in the OptionMenu element.
            :type options: list
            :ivar value: The value of the current chosen value in OptionMenu.
            :type value: string
            :ivar menu: The OptionMenu element used to choose values from a preset list of values.
            :type menu: OptionMenu
            :function grid: Sets the location of the Label and OptionMenu elements on content.
            :function set_option: Replaces the current chosen value of the OptionMenu element with a new value.
        """
        content = None
        label = None
        options = None
        value = None
        menu = None
        def __init__(self,content,master,title,options):
            """
            Initializes and instance of OptionMenuElement.
                :argument content: The Frame which the Label and OptionMenu elements will be displayed upon.
                :type content: Frame
                :argument master: The master frame which all elements, including content, are added to.
                :type master: instance
                :argument title: The text stored in the Label element next to the OptionMenu element.
                :type title: string
                :argument options: The list of values stored as choosable options in the OptionMenu element.
                :type options: list
            """
            self.content = content
            self.options = options
            self.value = StringVar(master, value=self.options[0])
            self.label = Label(content, text=title)
            self.menu = apply(OptionMenu, (content, self.value) + tuple(self.options))
            self.menu.pack()
        def grid(self, row, column):
            """
            Sets the location of the Label and OptionMenu elements on content.
                :argument row: The row (y axis) which the Label and Entry elements will be put at.
                :type row: int
                :argument column: The column (x axis) which the Label and Entry elements will be put at.
                :type column: int
            """
            self.label.grid(column=column, row=row, sticky=W, padx=5)
            self.menu.grid(column=column, row=row, sticky=E, padx=5)
        def set_option(self,option):
            """
            Replaces the current chosen value of the OptionMenu element with a new value.
                :argument option: The new replacement value.
                :type text: string, int, float
                """
            self.value.set(option)
            self.menu = apply(OptionMenu, (self.content, self) + tuple(self.options))

    class CheckBoxElement:
        """
        An object used to store and manipulate a variable and a Checkbutton element on ScarberryGui.
            :ivar value: The current on/off value of the Checkbutton element.
            :type value: boolean
            :ivar check_box: The Checkbutton element used to set the on/off of value.
            :type check_boc: Checkbutton
            :ivar padx: The empty space added onto the left and right of the Checkbutton element.
            :type padx: int
            :ivar sticky: The cardinal wall which the Checkbutton element will be affixed to.
            :type sticky: N,E,S,W
            :function grid: Sets the location of the Checkbutton element on content.
        """
        value = None
        check_box = None
        padx = None
        sticky = None
        def __init__(self,content,title,padx,sticky):
            """
            Initializes an instance of CheckBoxElement.
                :argument content: The Frame which the Label and OptionMenu elements will be displayed upon.
                :type content: Frame
                :argument title: The displayed next to the check box.
                :type title: string
                :argument padx: The empty space added onto the left and right of the Checkbutton element.
                :type padx: int
                :argument sticky: The cardinal wall which the Checkbutton element will be affixed to.
                :type sticky: N,E,S,W
            """
            self.padx = padx
            self.sticky = sticky
            self.value = IntVar()
            self.check_box = Checkbutton(content, text=title,variable=self.value)
            self.check_box.pack()
        def grid(self,row,column):
            """
            Sets the location of the Checkbutton element on content.
                :argument row: The row (y axis) which the Label and Entry elements will be put at.
                :type row: int
                :argument column: The column (x axis) which the Label and Entry elements will be put at.
                :type column: int
            """
            self.check_box.grid(column=column, row=row, sticky=self.sticky, padx=self.padx)

    class TextElement:
        """
        An object used to store and manipulate a LabelFrame and Text element as one unit on ScarberryGui.
            :ivar frame: The LabelFrame element encompassing and identifying the Text element.
            :type frame: LabelFrame
            :ivar text: The Text element used to display text.
            :type text: Text
            :function grid: Sets the location of the LabelFrame and Text elements and their rowspan.
        """
        frame = None
        text = None
        def __init__(self,content,title,height,width):
            """
            Initializes an instance of TextElement.
                :argument content: The Frame which the Label and OptionMenu elements will be displayed upon.
                :type content: Frame
                :argument title: The text stored on the LabelFrame element above the Text element.
                :type title: string
                :argument height: The number of characters tall the Text element will be.
                :type height: int
                :argument width: The number of characters wide the Text element will be.
                :type width: int
            """
            self.frame = LabelFrame(content, text=title, padx=5, pady=5)
            self.text = Text(self.frame, height=height, width=width)
            self.text.config(state=DISABLED)
            self.text.pack()
        def grid(self,column,rows):
            """
            Sets the column location of the LabelFrame and Text elements and their rowspan.
                :argument rows: The number of rows (y axis) which the LabelFrame and Text elements will be covering.
                :type rows: int
                :argument column: The column (x axis) which the LabelFrame and Text elements will be put at.
                :type column: int
                """
            self.frame.grid(column=column,row=0,columnspan=2,rowspan=rows,sticky=N)

def choose_print(gui, label, text):
    """
    Evaluates whether or not text shoud be printed to the Python Shell or an interface.
        :argument gui: The interface text will be printed onto.
        :type gui: ScarberryGui
        :argument label: The string used to identify which Text element text should be printed to.
        :type label: string
        :argument text: The text which will either be printed to the Python Shell or gui.
        :type text:
    """
    widget = None
    if gui is None:
        print text
    else:
        if label == 'arduino':
            widget = gui.arduino_controller_text.text
        elif label == 'camera':
            widget = gui.ximea_controller_text.text
        elif label == 'save':
            widget = gui.save_image_text.text
        elif label == 'data':
            widget = gui.data_image_text.text
        widget.config(state="normal")
        widget.insert('0.0', '{}\n'.format(text))
        widget.config(state=DISABLED)