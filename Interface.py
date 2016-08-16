from Tkinter import *
import ttk
import Main
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
    arduino_controller_text = None
    ximea_client_text = None
    process_image_text = None

    def __init__(self):
        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.wm_title('Project Scarberry')
        self.master.wm_iconbitmap('icon\\butterflybrown-256.ico')
        self.content = ttk.Frame(self.master)
        frame = ttk.Frame(self.content, borderwidth=2, relief='sunken')

        menu_bar = Menu(self.master, tearoff=0)
        self.master.config(menu=menu_bar)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label='Exit')
        menu_bar.add_cascade(label='File', menu=file_menu)
        settings_menu = Menu(menu_bar)
        preset_menu = Menu(settings_menu)
        preset_menu.add_command(label='Open Presets',command=self.open_settings)
        preset_menu.add_command(label='Set Presets', command=self.set_presets)
        preset_menu.add_command(label='Reset to Presets',command=self.set_entry)
        settings_menu.add_cascade(label='Presets', menu=preset_menu, underline=0)
        menu_bar.add_cascade(label='Settings', menu=settings_menu)
        menu_bar.add_command(label='About')

        west_list = []
        east_list = []
        extender = Label(self.content,text='                                      ')
        self.com = StringVar()
        com_label = Label(self.content,text='Serial Port:   COM')
        west_list.append(com_label)
        self.com_entry = Entry(self.content,width=3,textvariable=self.com)
        east_list.append(self.com_entry)
        self.runtime = StringVar()
        runtime_label = Label(self.content,text='RunTime:  ')
        west_list.append(runtime_label)
        self.runtime_entry = Entry(self.content,width=5,textvariable=self.runtime)
        east_list.append(self.runtime_entry)
        self.framerate = StringVar()
        framerate_label = Label(self.content,text='Framerate:  ')
        west_list.append(framerate_label)
        self.framerate_entry = Entry(self.content,width=5,textvariable=self.framerate)
        east_list.append(self.framerate_entry)
        self.strobecount = StringVar()
        strobecount_label = Label(self.content,text='Strobe Count:  ')
        west_list.append(strobecount_label)
        self.strobecount_entry = Entry(self.content,width=5,textvariable=self.strobecount)
        east_list.append(self.strobecount_entry)
        self.dutycycle = StringVar()
        dutycycle_label = Label(self.content,text='Duty Cycle:        0.')
        west_list.append(dutycycle_label)
        self.dutycycle_entry = Entry(self.content,width=2,textvariable=self.dutycycle)
        east_list.append(self.dutycycle_entry)
        self.thresh = StringVar()
        thresh_label = Label(self.content,text='Thresh Limit:  ')
        west_list.append(thresh_label)
        self.thresh_entry = Entry(self.content,width=5,textvariable=self.thresh)
        east_list.append(self.thresh_entry)

        self.blur_options = self.generate_optionmenu_elements(15, 3, 2)
        self.blur = IntVar(self.master,value=self.blur_options[0])
        blur_label =  Label(self.content,text='Blur Val:  ')
        west_list.append(blur_label)
        self.blur_menu = apply(OptionMenu, (self.content, self.blur) + tuple(self.blur_options))
        east_list.append(self.blur_menu)
        self.blur_menu.pack()
        self.gain_options = self.generate_optionmenu_elements(7, 0, 1)
        self.gain = IntVar(self.master,value=self.gain_options[6])
        gain_label =  Label(self.content,text='Gain Val:  ')
        west_list.append(gain_label)
        self.gain_menu = apply(OptionMenu, (self.content, self.gain) + tuple(self.gain_options))
        east_list.append(self.gain_menu)
        self.gain_menu.pack()

        self.save_pic = IntVar()
        self.save_pic_box = Checkbutton(self.content, text='Save Pic', variable=self.save_pic)
        west_list.append(self.save_pic_box)
        east_list.append(Label(self.content))
        self.save_pic_box.pack()
        self.contour_pic = IntVar()
        self.contour_pic_box = Checkbutton(self.content, text='Contour Pic', variable=self.contour_pic)
        west_list.append(self.contour_pic_box)
        east_list.append(Label(self.content))
        self.contour_pic_box.pack()

        start_button = Button(self.content, text='   Start   ',command=self.start_main)
        start_button.pack()
        west_list.append(start_button)
        abort_button = Button(self.content, text='   Abort   ')
        start_button.pack()
        east_list.append(abort_button)

        text_hight = 15
        text_width = 30
        arduino_controller_frame = LabelFrame(self.content, text='ArduinoController', padx=5, pady=5)
        self.arduino_controller_text = Text(arduino_controller_frame, height=text_hight, width=text_width)
        self.arduino_controller_text.config(state=DISABLED)
        self.arduino_controller_text.pack()
        ximea_client_frame = LabelFrame(self.content, text='XimeaClient', padx=5, pady=5)
        self.ximea_client_text = Text(ximea_client_frame, height=text_hight, width=text_width)
        self.ximea_client_text.config(state=DISABLED)
        self.ximea_client_text.pack()
        process_image_frame = LabelFrame(self.content, text='ProcessImage', padx=5, pady=5)
        self.process_image_text = Text(process_image_frame, height=text_hight, width=text_width)
        self.process_image_text.config(state=DISABLED)
        self.process_image_text.pack()

        self.content.grid(column=0, row=0)
        columns = 6
        rows = 15
        frame.grid(column=0, row=0, columnspan=columns, rowspan=rows)

        extender.grid(column=0, row=0,sticky=W)
        west_count = 0
        for element in west_list:
            element.grid(column=0, row=west_count, sticky=W, padx=5)
            west_count+=1
        east_count = 0
        for element in east_list:
            element.grid(column=0, row=east_count, sticky=E, padx=5)
            east_count += 1

        arduino_controller_frame.grid(column=1,row=0,columnspan=2,rowspan=rows,sticky=N,)
        ximea_client_frame.grid(column=1+(columns/3),row=0,columnspan=2,rowspan=rows,sticky=N)
        process_image_frame.grid(column=1+((columns/3)*2),row=0,columnspan=2,rowspan=rows,sticky=N)

    def start(self):
        self.master.mainloop()

    def generate_optionmenu_elements(self, number, start, increment):
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu

    def open_settings(self):
        subprocess.Popen(["notepad.exe", Main.settings_file_directory])

    def set_entry(self):
        settings = Main.get_settings_dic(["Main","Arduino", "XimeaClient", "ProcessImage"])
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

    def set_main_values(self):
        new_main_values = [1, self.runtime.get()]
        new_arduino_values = [self.com.get(), self.framerate.get(), self.strobecount.get(),(float(self.dutycycle.get())) / 100]
        new_camera_values = [self.gain.get()]
        new_process_values = [self.blur.get(), self.thresh.get(), self.save_pic.get(), self.contour_pic.get()]
        Main.set_values(new_main_values, new_arduino_values, new_camera_values, new_process_values)

    def set_presets(self):
        self.set_main_values()
        Main.save_settings()

    def start_main(self):
        self.set_main_values()
        Main.start_threads(self)

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

def main():
    gui = ScarberryGui(None)

if __name__ == '__main__':
    main()