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
    arduino_controller_frame = None
    arduino_controller_text = None
    ximea_client_frame = None
    ximea_client_text = None
    process_image_frame = None
    process_image_text = None
    element_list = []

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
                              command=lambda:Main.start_threads(self.get_entry_values_dic(),gui=self))
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
        for element in self.element_list:
            element.grid(list_count,0)
            list_count+=1

        directory_button.grid(column=0, row=list_count, padx=5)
        start_button.grid(column=0, row=list_count+1, sticky=W, padx=5)
        abort_button.grid(column=0, row=list_count+1, sticky=E, padx=5)
        self.arduino_controller_frame.grid(column=1,row=0,columnspan=2,rowspan=rows,sticky=N,)
        self.ximea_client_frame.grid(column=1+(columns/3),row=0,columnspan=2,rowspan=rows,sticky=N)
        self.process_image_frame.grid(column=1+((columns/3)*2),row=0,columnspan=2,rowspan=rows,sticky=N)

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
        self.element_list.extend([self.com,
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
        self.element_list.extend([self.extension,
                                  self.blur,
                                  self.gain])

    def format_texts(self):
        text_height = 17
        text_width = 30
        self.arduino_controller_frame = LabelFrame(self.content, text='ArduinoController', padx=5, pady=5)
        self.arduino_controller_text = Text(self.arduino_controller_frame, height=text_height, width=text_width)
        self.arduino_controller_text.config(state=DISABLED)
        self.arduino_controller_text.pack()
        self.ximea_client_frame = LabelFrame(self.content, text='XimeaClient', padx=5, pady=5)
        self.ximea_client_text = Text(self.ximea_client_frame, height=text_height, width=text_width)
        self.ximea_client_text.config(state=DISABLED)
        self.ximea_client_text.pack()
        self.process_image_frame = LabelFrame(self.content, text='ProcessImage', padx=5, pady=5)
        self.process_image_text = Text(self.process_image_frame, height=text_height, width=text_width)
        self.process_image_text.config(state=DISABLED)
        self.process_image_text.pack()

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
        self.set_entry(Main.get_settings_dic(['Main','Arduino','XimeaClient','ProcessImage']))

    def set_entry(self,settings):
        main_values = settings.get("Main")
        arduino_values = settings.get("Arduino")
        camera_values = settings.get("XimeaClient")
        process_values = settings.get("ProcessImage")
        self.image_directory = process_values[2]
        self.com.entry.delete(0,END)
        self.com.entry.insert(0,arduino_values[0])
        self.runtime.entry.delete(0, END)
        self.runtime.entry.insert(0,main_values[1])
        self.framerate.entry.delete(0, END)
        self.framerate.entry.insert(0,arduino_values[1])
        self.strobecount.entry.delete(0, END)
        self.strobecount.entry.insert(0,arduino_values[2])
        self.dutycycle.entry.delete(0, END)
        self.dutycycle.entry.insert(0,(arduino_values[3])[arduino_values[3].index('.')+1:])
        self.thresh.entry.delete(0, END)
        self.thresh.entry.insert(0,process_values[1])
        self.name.entry.delete(0, END)
        self.name.entry.insert(0, process_values[3])
        self.padding.entry.delete(0, END)
        self.padding.entry.insert(0, process_values[4])
        self.extension.value.set(process_values[5])
        self.extension.menu = apply(OptionMenu, (self.content, self.extension) + tuple(self.extension.options))
        self.blur.value.set(process_values[0])
        self.blur.menu = apply(OptionMenu, (self.content, self.blur) + tuple(self.blur.options))
        self.gain.value.set(camera_values[0])
        self.gain.menu = apply(OptionMenu, (self.content, self.gain) + tuple(self.gain.options))

    def get_entry_values_dic(self):
        new_main_values = [1, self.runtime.value.get()]
        new_arduino_values = [self.com.value.get(),
                              self.framerate.value.get(),
                              self.strobecount.value.get(),
                              float('.' + self.dutycycle.value.get())]
        new_camera_values = [self.gain.value.get()]
        new_process_values = [self.blur.value.get(),
                              self.thresh.value.get(),
                              self.image_directory,
                              self.name.value.get(),
                              self.padding.value.get(),
                              self.extension.value.get()]
        return {'Main':new_main_values,
                'Arduino':new_arduino_values,
                'XimeaClient':new_camera_values,
                'ProcessImage':new_process_values}

    def set_presets(self):
        Main.save_settings(self.get_entry_values_dic())

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

def choose_print(gui, text, string):
    widget = None
    if gui is None:
        print string
    else:
        if text == 'arduino':
            widget = gui.arduino_controller_text
        elif text == 'camera':
            widget = gui.ximea_client_text
        elif text == 'process':
            widget = gui.process_image_text
        widget.config(state="normal")
        widget.insert('0.0', '{}\n'.format(string))
        widget.config(state=DISABLED)