from Tkinter import *
import tkFileDialog
import ttk
import Main
import subprocess

class ScarberryGui:
    image_directory = ''
    master = None
    content = None
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
    draw_vector = None
    draw_count = None
    arduino_controller_text = None
    ximea_client_text = None
    process_image_text = None
    option_elements = []
    text_elements = []

    def __init__(self):
        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.wm_title('Project Scarberry')
        self.master.wm_iconbitmap('icon\\butterflybrown-256.ico')
        self.content = ttk.Frame(self.master)
        frame = ttk.Frame(self.content, borderwidth=2, relief='sunken')
        extender = Label(self.content, text='                                              ')

        self.format_menu()
        self.format_entrys()
        self.format_optionmenus()
        directory_button = Button(self.content,
                                  text='   Set Pic Directory   ',
                                  command=self.set_directory)
        directory_button.pack()
        start_button = Button(self.content,
                              text='   Start   ',
                              command=lambda:Main.start_threads(self.get_entry_values_dict(), gui=self))
        start_button.pack()
        abort_button = Button(self.content, text='   Abort   ',)
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
        self.draw_roi = ScarberryGui.CheckBoxElement(self.content,"Roi ",20,W)
        self.draw_roi.grid(list_count+1,0)
        self.draw_centroid = ScarberryGui.CheckBoxElement(self.content,"Centroid ",2,E)
        self.draw_centroid.grid(list_count+1,0)
        self.draw_vector = ScarberryGui.CheckBoxElement(self.content,"Vector ",20,W)
        self.draw_vector.grid(list_count+2,0)
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

    def format_entrys(self):
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
        self.extension = ScarberryGui.OptionMenuElement(self.content,self.master,'Pic Extension: ',['.TIF','.png','.jpg','.gif'])
        self.blur = ScarberryGui.OptionMenuElement(self.content,self.master,'Blur Val: ',self.generate_optionmenu_elements(15, 3, 2))
        self.gain = ScarberryGui.OptionMenuElement(self.content,self.master,'Gain Val:  ',self.generate_optionmenu_elements(7, 0, 1))
        self.shrink = ScarberryGui.OptionMenuElement(self.content,self.master,'Shrink Val:  ',['1','2','4','8','16','32'])
        self.option_elements.extend([self.extension,
                                     self.blur,
                                     self.gain,
                                     self.shrink])

    def format_texts(self):
        text_height = 25
        text_width = 30
        self.arduino_controller_text = ScarberryGui.TextElement(self.content,'ArduinoController',text_height,text_width)
        self.ximea_client_text = ScarberryGui.TextElement(self.content,'XimeaClient',text_height,text_width)
        self.process_image_text = ScarberryGui.TextElement(self.content, 'ProcessImage',text_height,text_width)
        self.text_elements = [self.arduino_controller_text,
                              self.ximea_client_text,
                              self.process_image_text]

    def start(self):
        self.master.mainloop()

    def set_directory(self):
        self.image_directory = tkFileDialog.askdirectory()

    def generate_optionmenu_elements(self, number, start, increment):
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu

    def open_settings(self):
        subprocess.Popen(["notepad.exe", Main.settings_file_directory])

    def open_images(self):
        print self.image_directory
        subprocess.Popen(["explorer.exe", "{}".format(self.image_directory.replace('/','\\'))])#"""{}".format(self.image_directory)])

    def open_data(self):
        print self.image_directory + '/data'
        subprocess.Popen(["explorer.exe", "{}\\data".format(self.image_directory.replace('/','\\'))])#"""{}".format(self.image_directory)])

    def reset_to_preset(self):
        self.set_entry(Main.get_settings_dict(['Main', 'Arduino', 'XimeaClient', 'ProcessImage']))

    def set_entry(self,settings):
        main_values = settings.get("Main")
        arduino_values = settings.get("Arduino")
        camera_values = settings.get("XimeaClient")
        process_values = settings.get("ProcessImage")
        self.image_directory = process_values.get("ImageDirectory")
        self.com.entry.delete(0,END)
        self.com.entry.insert(0,arduino_values.get("SerialPort"))
        self.runtime.entry.delete(0, END)
        self.runtime.entry.insert(0,main_values.get("RunTime"))
        self.framerate.entry.delete(0, END)
        self.framerate.entry.insert(0,arduino_values.get("FrameRate"))
        self.strobecount.entry.delete(0, END)
        self.strobecount.entry.insert(0,arduino_values.get("StrobeCount"))
        self.dutycycle.entry.delete(0, END)
        raw_dutycycle = arduino_values.get("DutyCycle")
        self.dutycycle.entry.insert(0,(raw_dutycycle)[raw_dutycycle.index('.')+1:])
        self.thresh.entry.delete(0, END)
        self.thresh.entry.insert(0,process_values.get("ThreshLimit"))
        self.name.entry.delete(0, END)
        self.name.entry.insert(0, process_values.get("BaseName"))
        self.padding.entry.delete(0, END)
        self.padding.entry.insert(0, process_values.get("NumberPadding"))
        self.extension.value.set(process_values.get("FileExtension"))
        self.extension.menu = apply(OptionMenu, (self.content, self.extension) + tuple(self.extension.options))
        self.blur.value.set(process_values.get("BlurValue"))
        self.blur.menu = apply(OptionMenu, (self.content, self.blur) + tuple(self.blur.options))
        self.gain.value.set(camera_values.get("Gain"))
        self.gain.menu = apply(OptionMenu, (self.content, self.gain) + tuple(self.gain.options))
        self.shrink.value.set(camera_values.get("ShrinkQuotient"))
        self.shrink.menu = apply(OptionMenu, (self.content, self.shrink) + tuple(self.shrink.options))
        self.draw.value.set(process_values.get("SaveDraw"))
        self.draw_roi.value.set(process_values.get("DrawROIs"))
        self.draw_centroid.value.set(process_values.get("DrawCentroid"))
        self.draw_vector.value.set(process_values.get("DrawVector"))
        self.draw_count.value.set(process_values.get("DrawCount"))

    def get_entry_values_dict(self):
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
                              "DrawVector":self.draw_vector.value.get(),
                              "DrawCount":self.draw_count.value.get()}
        return {'Main':new_main_values,
                'Arduino':new_arduino_values,
                'XimeaClient':new_camera_values,
                'ProcessImage':new_process_values}

    def set_presets(self):
        Main.save_settings(self.get_entry_values_dict())

    class EntryElement:
        value = None
        label = None
        entry = None
        def __init__(self,content,title,width):
            self.value = StringVar()
            self.label = Label(content, text=title)
            self.entry = Entry(content, width=width, textvariable=self.value)
        def grid(self,row,column):
            self.label.grid(column=column, row=row, sticky=W, padx=5)
            self.entry.grid(column=column, row=row, sticky=E, padx=5)

    class OptionMenuElement:
        label = None
        options = None
        value = None
        menu = None
        def __init__(self,content,master,title,options):
            self.options = options
            self.value = StringVar(master, value=self.options[0])
            self.label = Label(content, text=title)
            self.menu = apply(OptionMenu, (content, self.value) + tuple(self.options))
            self.menu.pack()
        def grid(self, row, column):
            self.label.grid(column=column, row=row, sticky=W, padx=5)
            self.menu.grid(column=column, row=row, sticky=E, padx=5)

    class CheckBoxElement:
        value = None
        check_box = None
        padx = None
        sticky = None
        def __init__(self,content,title,padx,sticky):
            self.padx = padx
            self.sticky = sticky
            self.value = IntVar()
            self.check_box = Checkbutton(content, text=title,variable=self.value)
            self.check_box.pack()
        def grid(self,row,column):
            self.check_box.grid(column=column, row=row, sticky=self.sticky, padx=self.padx)

    class TextElement:
        frame = None
        text = None
        def __init__(self,content,title,height,width):
            self.frame = LabelFrame(content, text=title, padx=5, pady=5)
            self.text = Text(self.frame, height=height, width=width)
            self.text.config(state=DISABLED)
            self.text.pack()
        def grid(self,column,rows):
            self.frame.grid(column=column,row=0,columnspan=2,rowspan=rows,sticky=N)

def choose_print(gui, text, string):
    widget = None
    if gui is None:
        print string
    else:
        if text == 'arduino':
            widget = gui.arduino_controller_text.text
        elif text == 'camera':
            widget = gui.ximea_client_text.text
        elif text == 'process':
            widget = gui.process_image_text.text
        widget.config(state="normal")
        widget.insert('0.0', '{}\n'.format(string))
        widget.config(state=DISABLED)