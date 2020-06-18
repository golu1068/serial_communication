## google cloud console
import serial
import tkinter as tk 
from tkinter import ttk 
import serial.tools.list_ports
from time import sleep
import threading
from functools import partial
from pkg import Initialization, tx_power, load_time, get_cmd, reset_cmd, factory_reset_cmd, data_rate
from tkinter import *
#################################################################################

def defocus(event):
    event.widget.master.focus_set()
#    event.widget.master.state = 'normal'
#    Port_name.takefocus = False
#    Port_name.state('readonly')
#b'\xe0\x07\x11\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80'
aa=1;
def go_to_sub(ser, text_out, pkg):
    global aa
    ser.reset_input_buffer()
    ser.reset_output_buffer()

#    ser.write(bytes('7e0080401010000', encoding='ascii')) 
    ser.write(bytes.fromhex(pkg))

    while True:
        data = ser.read(size=9999)
        if len(data) > 0:
            print(len(data))
            print ('Got:', data)
            break
        
        if (aa==0):
            break
        
    data_hex =data.hex()
    pkg = get_cmd(data_hex) 
    
    text_out.config(state=NORMAL)
    text_out.insert(INSERT,pkg[0])
    text_out.insert(INSERT,'\n')
    text_out.insert(INSERT,pkg[1])
    text_out.config(state=DISABLED)
        
    ser.close()

def defocus(event):
    event.widget.master.focus_set()
#    event.widget.master.state = 'normal'
#    Port_name.takefocus = False
#    Port_name.state('readonly')
    
def go_to_Initialization(Port_name, e1, e2, text_out, *args):
    port_name = Port_name.get()
    bdrate = e1.get()
    bytesize = e2.get()
    port_name_li = port_name.split()
#    ser = serial.Serial(port=port_name_li[0], baudrate=bdrate, bytesize=int(bytesize), 
#                        stopbits=1)
#    if (ser.isOpen() == True):
    if (args[0] == 'init'):
        pkg = Initialization()
    elif (args[0] == 'tx_power'):
        pkg = tx_power()
    elif (args[0] == 'ld_time'):
        pkg = load_time()
    elif (args[0] == 'get_cmd'):
        pkg = get_cmd('read')
    elif (args[0] == 'reset'):
        pkg = reset_cmd()
    elif (args[0] == 'fact_res'):
        pkg = factory_reset_cmd()
    elif (args[0] == 'data_rate'):
        pkg = data_rate()
    print(str(int(len(pkg)/2))+ 'B')
    print(pkg)
    text_out.config(state=NORMAL)
    text_out.delete(1.0, END)
#    text_out.insert(INSERT,pkg)
    text_out.config(state=DISABLED)
    
#    t1 = threading.Thread(target=go_to_sub, args=(ser,text_out,pkg,))
#    t1.start()
    
    
def quit_btn(master):
    global aa
    aa=0;
    if (aa==0):
        master.destroy()
class make_gui():
    def __init__(self, **kwargs):
        super(make_gui, self).__init__(**kwargs)
        ###############################################################
        port_list=[];
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            port_list.append(p)
        port_list = tuple(port_list)
        #############################################################
        master = tk.Tk() 
        master.geometry('655x450+400+200')
        master.resizable(0, 0)
        master.title('On Board Computer Stimulator')
        master.iconbitmap(r'E:\spyder_code\New_folder\multipath_test\favicon.ico')
        master.configure(bg='white')
        
        bg_color = 'light Blue'
        
        
        master_frame = Frame(master, bg='white', width = 640, height=240, bd=1, relief=RIDGE)
        master_frame.grid(row=0, column=0, sticky=N, padx=5, pady=20)
        master_frame.grid_propagate(False)
        
        
        frame0 = Frame(master_frame,  bg='white', width=295, height=20)
        frame0.grid(row=0, column=0, sticky=N, pady=3)
        frame0.grid_propagate(False)
        self.l11 = ttk.Label(frame0, text = "RS422 Port Configuration :",
                font = ("Times New Roman", 12), background='white')
        self.l11.grid(row = 0, column = 0)
        
        frame1 = Frame(master_frame, width=300, bd=3, relief=RIDGE, height=140, bg='light blue')
        frame1.grid(row=0, column=0, padx=10, pady=26, sticky=N)
        frame1.grid_propagate(False) 
        
        frame20 = Frame(master_frame,  bg='white', width=295, height=20)
        frame20.grid(row=0, column=1, sticky=N, pady=3)
        frame20.grid_propagate(False)
        self.l22 = ttk.Label(frame20, text = "Command Message :",
                font = ("Times New Roman", 12), background='white')
        self.l22.grid(row = 0, column = 1)
        
        frame2 = Frame(master_frame, width=295, bd=3, relief=RIDGE, height=200, bg='light Blue')
        frame2.grid(row=0, column=1, padx=8, pady=26, sticky=N)
        frame2.grid_propagate(False)
        
        frame30 = Frame(master,  bg='white', width=295, height=20)
        frame30.grid(row=1, column=0, sticky='wn', pady=0, padx=50)
        frame30.grid_propagate(False)
        self.l33 = ttk.Label(frame30, text = "Received Response :",
                font = ("Times New Roman", 12), background='white')
        self.l33.grid(row = 1, column = 0, sticky=N)
        
        frame3 = Frame(master, width=550, bd=5, relief=RIDGE, height=100, bg='light Blue')
        frame3.grid(row=1, column=0, sticky=S, columnspan=4, padx=10, pady=22)
        frame3.grid_propagate(False)
        self.text = Text(frame3, height=5.5, width=67, bg='black', fg='white', cursor= 'xterm',insertbackground ='white')
#        text.pack()
#        text.insert(INSERT, "Hello.....")
#        text.insert(END, "Bye Bye.....")
#        print(text.get("1.0", "end-2c"))
        self.text.grid(row=1, column=0, padx=0)
#        self.text.bind("<Key>", lambda a: "break")
        self.text.config(state=DISABLED)
        

        self.l1 = ttk.Label(frame1, text = "Baud Rate :",
                font = ("Times New Roman", 10), background=bg_color)
        self.l1.grid(row = 10, column = 0,  padx = 0, pady = 5)
        
        self.e1 = ttk.Entry(frame1, width = 30, foreground='Grey')
        self.e1.insert(10, '9600')
        self.e1.grid(row= 10, column=1)
        
        self.err_msg = ttk.Label(frame1, font = ("Times New Roman", 10), foreground='red')
        
        self.reg = master.register(self.callback_baud)
        self.e1.config(validate ="all",  
                 validatecommand =(self.reg, '%i', '%S'))
        
        self.l2 = ttk.Label(frame1, text = "Port Name :", 
                font = ("Times New Roman", 10), background=bg_color)
        self.l2.grid(row = 20, column = 0,  padx = 10, pady = 5) 
        
        n = tk.StringVar() 
        self.Port_name = ttk.Combobox(frame1, width = 27, textvariable = n, foreground='Grey', state='readonly')
        self.Port_name.set('Select Port name')
        self.Port_name['values'] = port_list
        self.Port_name.bind("<FocusIn>", defocus)
        self.Port_name.current(0)
        self.Port_name.grid(row = 20, column = 1) 
        
        self.l3 = ttk.Label(frame1, text = "Byte Size  :",
                font = ("Times New Roman", 10), background=bg_color)
        self.l3.grid(row = 30, column = 0,  padx = 0, pady = 5)
        
        self.e2 = ttk.Entry(frame1, width = 30, foreground='black')
        self.e2.insert(10, '8')
        self.e2.grid(row=30, column=1)
        
        
         ######################################################################
        self.b2 = tk.Button(frame2, text='Initialization', command=partial(go_to_Initialization, self.Port_name, 
                                                                           self.e1, self.e2, self.text, 'init'),
                            background="light sea green", width=10)
        self.b2.grid(row=40, column=0, sticky =W, pady=10, padx=8)
        self.b3 = tk.Button(frame2, text='Tx_power', command=partial(go_to_Initialization, self.Port_name, 
                                                                     self.e1, self.e2, self.text, 'tx_power'),
                            background="light sea green", width=10)
        self.b3.grid(row=40, column=1, pady=10,padx=8)
        self.b4 = tk.Button(frame2, text='Load_time', command=partial(go_to_Initialization, self.Port_name, 
                                                                      self.e1, self.e2, self.text, 'ld_time'),
                            background="light sea green", width=10)
        self.b4.grid(row=40, column=2, sticky =W, pady=10, padx=8)
        ######
        self.b5 = tk.Button(frame2, text='Get_cmd', command=partial(go_to_Initialization, self.Port_name, 
                                                                    self.e1, self.e2, self.text, 'get_cmd'),
                            background="light sea green", width=10)
        self.b5.grid(row=41, column=0, sticky =W, pady=10, padx=8)
        self.b6 = tk.Button(frame2, text='Reset', command=partial(go_to_Initialization, self.Port_name, 
                                                                  self.e1, self.e2, self.text, 'reset'),
                            background="light sea green", width=10)
        self.b6.grid(row=41, column=1, pady=10)
        self.b7 = tk.Button(frame2, text='Factory_reset', command=partial(go_to_Initialization, 
                                                                          self.Port_name, self.e1, self.e2, self.text, 'fact_res'),
                            background="light sea green", width=10)
        self.b7.grid(row=41, column=2, sticky =W, pady=10, padx=8)
        
        self.b8 = tk.Button(frame2, text='Data_rate', command=partial(go_to_Initialization, 
                                                                      self.Port_name, self.e1, self.e2, self.text, 'data_rate'),
                            background="light sea green", width=10)
        self.b8.grid(row=42, column=1, pady=10)
        
        #####################################################################
        self.b1 = tk.Button(frame1, text='Quit', command=partial(quit_btn, master), width=10, background="red")
        self.b1.grid(row=60, column=0,pady=15, padx=10)
        
        master.mainloop()
    
    def callback_baud(self, input, num_check):
        if input.isdigit():
            if (input == '0'):
                self.e1.config(foreground='black')
            ###############################################
            if (num_check.isdigit() == False):
                self.err_msg.grid(row=0, column=1, padx=15)
                self. err_msg.config(text='Please enter a number')
                return False
            else:
                self.err_msg.grid_forget()
    #            err_msg.config(text='')
            ##############################################
        return True


if __name__ == "__main__":
    make_gui()
