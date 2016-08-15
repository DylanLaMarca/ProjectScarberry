from Tkinter import *
import ttk
import time

class ScarberryGui:
    master = None
    content = None
    com_entry = None
    runtime_entry = None
    framerate_entry = None
    strobecount_entry = None
    dutycycle_entry = None
    thresh_entry = None
    blur_menu = None
    gain_menu = None
    arduino_controller_text = None
    ximea_client_text = None
    process_image_text = None

    def __init__(self,start_button_function):
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
        preset_menu.add_command(label='Open Presets')
        preset_menu.add_command(label='Set Presets')
        preset_menu.add_command(label='Reset to Presets')
        settings_menu.add_cascade(label='Presets', menu=preset_menu, underline=0)
        menu_bar.add_cascade(label='Settings', menu=settings_menu)
        menu_bar.add_command(label='About')

        west_list = []
        east_list = []
        extender = Label(self.content,text='                                      ')
        com = StringVar()
        com_label = Label(self.content,text='Serial Port:   COM')
        west_list.append(com_label)
        self.com_entry = Entry(self.content,width=3,textvariable=com)
        east_list.append(self.com_entry)
        runtime = StringVar()
        runtime_label = Label(self.content,text='RunTime:  ')
        west_list.append(runtime_label)
        self.runtime_entry = Entry(self.content,width=5,textvariable=runtime)
        east_list.append(self.runtime_entry)
        framerate = StringVar()
        framerate_label = Label(self.content,text='Framerate:  ')
        west_list.append(framerate_label)
        self.framerate_entry = Entry(self.content,width=5,textvariable=framerate)
        east_list.append(self.framerate_entry)
        strobecount = StringVar()
        strobecount_label = Label(self.content,text='Strobe Count:  ')
        west_list.append(strobecount_label)
        self.strobecount_entry = Entry(self.content,width=5,textvariable=strobecount)
        east_list.append(self.strobecount_entry)
        dutycycle = StringVar()
        dutycycle_label = Label(self.content,text='Duty Cycle:        0.')
        west_list.append(dutycycle_label)
        self.dutycycle_entry = Entry(self.content,width=2,textvariable=dutycycle)
        east_list.append(self.dutycycle_entry)
        thresh = StringVar()
        thresh_label = Label(self.content,text='Thresh Limit:  ')
        west_list.append(thresh_label)
        self.thresh_entry = Entry(self.content,width=5,textvariable=thresh)
        east_list.append(self.thresh_entry)

        blur_options = self.generate_menu_elements(15,3,2)
        blur = IntVar(self.master,value=blur_options[0])
        blur_label =  Label(self.content,text='Blur Val:  ')
        west_list.append(blur_label)
        self.blur_menu = apply(OptionMenu, (self.content, blur) + tuple(blur_options))
        east_list.append(self.blur_menu)
        self.blur_menu.pack()
        gain_options = self.generate_menu_elements(7,0,1)
        gain = IntVar(self.master,value=gain_options[6])
        gain_label =  Label(self.content,text='Gain Val:  ')
        west_list.append(gain_label)
        self.gain_menu = apply(OptionMenu, (self.content, gain) + tuple(gain_options))
        east_list.append(self.gain_menu)
        self.gain_menu.pack()

        save_pic = IntVar()
        save_pic_box = Checkbutton(self.content, text='Save Pic', variable=save_pic)
        west_list.append(save_pic_box)
        east_list.append(Label(self.content))
        save_pic_box.pack()
        contour_pic = IntVar()
        contour_pic_box = Checkbutton(self.content, text='Contour Pic', variable=contour_pic)
        west_list.append(contour_pic_box)
        east_list.append(Label(self.content))
        contour_pic_box.pack()

        start_button = Button(self.content, text='   Start   ',command=start_button_function)
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

    def generate_menu_elements(self, number, start, increment):
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu

def chose_print(gui, text, string):
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