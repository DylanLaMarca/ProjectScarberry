from Tkinter import *
import ttk

class ScarberryGui:
    def __init__(self,start_button_function):
        master = Tk()
        master.resizable(0, 0)
        master.wm_title('Project Scarberry')
        master.wm_iconbitmap('icon\\butterflybrown-256.ico')
        content = ttk.Frame(master)
        frame = ttk.Frame(content, borderwidth=2, relief="sunken")

        menu_bar = Menu(master, tearoff=0)
        master.config(menu=menu_bar)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label="Exit")
        menu_bar.add_cascade(label="File", menu=file_menu)
        settings_menu = Menu(menu_bar)
        preset_menu = Menu(settings_menu)
        preset_menu.add_command(label="Open Presets")
        preset_menu.add_command(label="Set Presets")
        preset_menu.add_command(label="Reset to Presets")
        settings_menu.add_cascade(label='Presets', menu=preset_menu, underline=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        menu_bar.add_command(label="About")

        west_list = []
        east_list = []
        extender = Label(content,text="                                      ")
        com = StringVar()
        com_label = Label(content,text="Serial Port:   COM")
        west_list.append(com_label)
        com_entry = Entry(content,width=3,textvariable=com)
        east_list.append(com_entry)
        runtime = StringVar()
        runtime_label = Label(content,text="RunTime:  ")
        west_list.append(runtime_label)
        runtime_entry = Entry(content,width=5,textvariable=runtime)
        east_list.append(runtime_entry)
        framerate = StringVar()
        framerate_label = Label(content,text="Framerate:  ")
        west_list.append(framerate_label)
        framerate_entry = Entry(content,width=5,textvariable=framerate)
        east_list.append(framerate_entry)
        strobecount = StringVar()
        strobecount_label = Label(content,text="Strobe Count:  ")
        west_list.append(strobecount_label)
        strobecount_entry = Entry(content,width=5,textvariable=strobecount)
        east_list.append(strobecount_entry)
        dutycycle = StringVar()
        dutycycle_label = Label(content,text="Duty Cycle:        0.")
        west_list.append(dutycycle_label)
        dutycycle_entry = Entry(content,width=2,textvariable=dutycycle)
        east_list.append(dutycycle_entry)
        thresh = StringVar()
        thresh_label = Label(content,text="Thresh Limit:  ")
        west_list.append(thresh_label)
        thresh_entry = Entry(content,width=5,textvariable=thresh)
        east_list.append(thresh_entry)

        blur_options = self.generate_menu_elements(15,3,2)
        blur = IntVar(master,value=blur_options[0])
        blur_label =  Label(content,text="Blur Val:  ")
        west_list.append(blur_label)
        blur_menu = apply(OptionMenu, (content, blur) + tuple(blur_options))
        east_list.append(blur_menu)
        blur_menu.pack()
        gain_options = self.generate_menu_elements(7,0,1)
        gain = IntVar(master,value=gain_options[6])
        gain_label =  Label(content,text="Gain Val:  ")
        west_list.append(gain_label)
        gain_menu = apply(OptionMenu, (content, gain) + tuple(gain_options))
        east_list.append(gain_menu)
        gain_menu.pack()

        save_pic = IntVar()
        save_pic_box = Checkbutton(content, text="Save Pic", variable=save_pic)
        west_list.append(save_pic_box)
        east_list.append(Label(content))
        save_pic_box.pack()
        contour_pic = IntVar()
        contour_pic_box = Checkbutton(content, text="Contour Pic", variable=contour_pic)
        west_list.append(contour_pic_box)
        east_list.append(Label(content))
        contour_pic_box.pack()

        start_button = Button(content, text="   Start   ",command=start_button_function)
        start_button.pack()
        west_list.append(start_button)
        abort_button = Button(content, text="   Abort   ")
        start_button.pack()
        east_list.append(abort_button)

        text_hight = 15
        text_width = 30
        arduino_controller_frame = LabelFrame(content, text="ArduinoController", padx=5, pady=5)
        arduino_controller_text = Text(arduino_controller_frame, height=text_hight, width=text_width)
        arduino_controller_text.config(state=DISABLED)
        arduino_controller_text.pack()
        ximea_client_frame = LabelFrame(content, text="XimeaClient", padx=5, pady=5)
        ximea_client_text = Text(ximea_client_frame, height=text_hight, width=text_width)
        ximea_client_text.config(state=DISABLED)
        ximea_client_text.pack()
        process_image_frame = LabelFrame(content, text="ProcessImage", padx=5, pady=5)
        process_image_text = Text(process_image_frame, height=text_hight, width=text_width)
        process_image_text.config(state=DISABLED)
        process_image_text.pack()

        content.grid(column=0, row=0)
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

        master.mainloop()

    def generate_menu_elements(self, number, start, increment):
        menu = []
        for count in range(number):
            menu.append(start + (increment * count))
        return menu


def main():
    gui = ScarberryGui()

if __name__ == "__main__":
    main()