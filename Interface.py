from Tkinter import *
import ttk
import Main
import XimeaClient
import subprocess

class ScarberryGui:
    master = None
    content = None
    com = None
    com_entry = None
    runtime = None
    runtime_entry = None
    framerate = None
    framerate_entry = None
    strobecount = None
    strobecount_entry = None
    dutycycle = None
    dutycycle_entry = None
    thresh = None
    thresh_entry = None
    blur = None
    blur_options = None
    blur_menu = None
    gain = None
    gain_options = None
    gain_menu = None
    save_pic = False
    save_pic_box = None
    contour_pic = False
    contour_pic_box = None
    arduino_controller_frame = None
    arduino_controller_text = None
    ximea_client_frame = None
    ximea_client_text = None
    process_image_frame = None
    process_image_text = None
    west_list = []
    east_list = []

    def __init__(self):
        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.wm_title('Project Scarberry')
        self.master.wm_iconbitmap('icon\\butterflybrown-256.ico')
        self.content = ttk.Frame(self.master)
        frame = ttk.Frame(self.content, borderwidth=2, relief='sunken')
        extender = Label(self.content, text='                                      ')
        self.format_menu()
        self.format_entrys()
        self.format_optionmenus()
        self.format_checkboxes()
        self.format_buttons()
        self.format_texts()
        self.content.grid(column=0, row=0)
        columns = 6
        rows = 15
        frame.grid(column=0, row=0, columnspan=columns, rowspan=rows)
        extender.grid(column=0, row=0,sticky=W)
        west_count = 0
        for element in self.west_list:
            element.grid(column=0, row=west_count, sticky=W, padx=5)
            west_count+=1
        east_count = 0
        for element in self.east_list:
            element.grid(column=0, row=east_count, sticky=E, padx=5)
            east_count += 1
        self.arduino_controller_frame.grid(column=1,row=0,columnspan=2,rowspan=rows,sticky=N,)
        self.ximea_client_frame.grid(column=1+(columns/3),row=0,columnspan=2,rowspan=rows,sticky=N)
        self.process_image_frame.grid(column=1+((columns/3)*2),row=0,columnspan=2,rowspan=rows,sticky=N)

    def format_menu(self):
        menu_bar = Menu(self.master, tearoff=0)
        self.master.config(menu=menu_bar)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label='Open Images',command=self.open_images)
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
        self.com = StringVar()
        com_label = Label(self.content, text='Serial Port:   COM')
        self.west_list.append(com_label)
        self.com_entry = Entry(self.content, width=3, textvariable=self.com)
        self.east_list.append(self.com_entry)
        self.runtime = StringVar()
        runtime_label = Label(self.content, text='RunTime:  ')
        self.west_list.append(runtime_label)
        self.runtime_entry = Entry(self.content, width=5, textvariable=self.runtime)
        self.east_list.append(self.runtime_entry)
        self.framerate = StringVar()
        framerate_label = Label(self.content, text='Framerate:  ')
        self.west_list.append(framerate_label)
        self.framerate_entry = Entry(self.content, width=5, textvariable=self.framerate)
        self.east_list.append(self.framerate_entry)
        self.strobecount = StringVar()
        strobecount_label = Label(self.content, text='Strobe Count:  ')
        self.west_list.append(strobecount_label)
        self.strobecount_entry = Entry(self.content, width=5, textvariable=self.strobecount)
        self.east_list.append(self.strobecount_entry)
        self.dutycycle = StringVar()
        dutycycle_label = Label(self.content, text='Duty Cycle:        0.')
        self.west_list.append(dutycycle_label)
        self.dutycycle_entry = Entry(self.content, width=2, textvariable=self.dutycycle)
        self.east_list.append(self.dutycycle_entry)
        self.thresh = StringVar()
        thresh_label = Label(self.content, text='Thresh Limit:  ')
        self.west_list.append(thresh_label)
        self.thresh_entry = Entry(self.content, width=5, textvariable=self.thresh)
        self.east_list.append(self.thresh_entry)

    def format_optionmenus(self):
        self.blur_options = self.generate_optionmenu_elements(15, 3, 2)
        self.blur = IntVar(self.master, value=self.blur_options[0])
        blur_label = Label(self.content, text='Blur Val:  ')
        self.west_list.append(blur_label)
        self.blur_menu = apply(OptionMenu, (self.content, self.blur) + tuple(self.blur_options))
        self.east_list.append(self.blur_menu)
        self.blur_menu.pack()
        self.gain_options = self.generate_optionmenu_elements(7, 0, 1)
        self.gain = IntVar(self.master, value=self.gain_options[6])
        gain_label = Label(self.content, text='Gain Val:  ')
        self.west_list.append(gain_label)
        self.gain_menu = apply(OptionMenu, (self.content, self.gain) + tuple(self.gain_options))
        self.east_list.append(self.gain_menu)
        self.gain_menu.pack()

    def format_checkboxes(self):
        self.save_pic = IntVar()
        self.save_pic_box = Checkbutton(self.content, text='Save Pic', variable=self.save_pic)
        self.west_list.append(self.save_pic_box)
        self.east_list.append(Label(self.content))
        self.save_pic_box.pack()
        self.contour_pic = IntVar()
        self.contour_pic_box = Checkbutton(self.content, text='Contour Pic', variable=self.contour_pic)
        self.west_list.append(self.contour_pic_box)
        self.east_list.append(Label(self.content))
        self.contour_pic_box.pack()

    def format_buttons(self):
        start_button = Button(self.content, text='   Start   ', command=self.start_main)
        start_button.pack()
        self.west_list.append(start_button)
        abort_button = Button(self.content, text='   Abort   ')
        abort_button.pack()
        self.east_list.append(abort_button)

    def format_texts(self):
        text_hight = 15
        text_width = 30
        self.arduino_controller_frame = LabelFrame(self.content, text='ArduinoController', padx=5, pady=5)
        self.arduino_controller_text = Text(self.arduino_controller_frame, height=text_hight, width=text_width)
        self.arduino_controller_text.config(state=DISABLED)
        self.arduino_controller_text.pack()
        self.ximea_client_frame = LabelFrame(self.content, text='XimeaClient', padx=5, pady=5)
        self.ximea_client_text = Text(self.ximea_client_frame, height=text_hight, width=text_width)
        self.ximea_client_text.config(state=DISABLED)
        self.ximea_client_text.pack()
        self.process_image_frame = LabelFrame(self.content, text='ProcessImage', padx=5, pady=5)
        self.process_image_text = Text(self.process_image_frame, height=text_hight, width=text_width)
        self.process_image_text.config(state=DISABLED)
        self.process_image_text.pack()

    def start(self):
        self.master.mainloop()

    def generate_optionmenu_elements(self, number, start, increment):
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu

    def open_settings(self):
        subprocess.Popen(["notepad.exe", Main.settings_file_directory])

    def open_images(self):
        path = subprocess.check_output(["echo", "%cd%"], shell=True)
        path = path[:len(path) - 2]
        path += "\\images"
        subprocess.Popen(["explorer.exe", "{}".format(path)])

    def reset_to_preset(self):
        self.set_entry(Main.get_settings_dic(['Main','Arduino','XimeaClient','ProcessImage']))

    def set_entry(self,settings):
        main_values = settings.get("Main")
        arduino_values = settings.get("Arduino")
        camera_values = settings.get("XimeaClient")
        process_values = settings.get("ProcessImage")
        self.com_entry.delete(0,END)
        self.com_entry.insert(0,arduino_values[0])
        self.runtime_entry.delete(0, END)
        self.runtime_entry.insert(0,main_values[1])
        self.framerate_entry.delete(0, END)
        self.framerate_entry.insert(0,arduino_values[1])
        self.strobecount_entry.delete(0, END)
        self.strobecount_entry.insert(0,arduino_values[2])
        self.dutycycle_entry.delete(0, END)
        self.dutycycle_entry.insert(0,(arduino_values[3])[arduino_values[3].index('.')+1:])
        self.thresh_entry.delete(0, END)
        self.thresh_entry.insert(0,process_values[1])
        self.blur.set(process_values[0])
        self.blur_menu = apply(OptionMenu, (self.content, self.blur) + tuple(self.blur_options))
        self.gain.set(camera_values[0])
        self.gain_menu = apply(OptionMenu, (self.content, self.gain) + tuple(self.gain_options))
        self.save_pic.set(process_values[2])
        self.save_pic_box = Checkbutton(self.content, text='Save Pic', variable=self.save_pic)
        self.contour_pic.set(process_values[3])
        self.contour_pic_box = Checkbutton(self.content, text='Contour Pic', variable=self.contour_pic)

    def get_entry_values_dic(self):
        new_main_values = [1, self.runtime.get()]
        new_arduino_values = [self.com.get(), self.framerate.get(), self.strobecount.get(),float('.' + self.dutycycle.get())]
        new_camera_values = [self.gain.get()]
        new_process_values = [self.blur.get(), self.thresh.get(), self.save_pic.get(), self.contour_pic.get()]
        return {'Main':new_main_values,'Arduino':new_arduino_values,'XimeaClient':new_camera_values,'ProcessImage':new_process_values}

    def set_presets(self):
        Main.save_settings(self.get_entry_values_dic())

    def start_main(self):
        Main.start_threads(self.get_entry_values_dic(),gui=self)

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