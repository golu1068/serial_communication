__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
## google cloud console
import serial
import tkinter as tk 
from tkinter import ttk 
import serial.tools.list_ports
from time import sleep
import threading
from functools import partial
from pkg import Initialization, tx_power, load_time, get_cmd, reset_cmd, factory_reset_cmd, data_rate
from pkg import acknowledgment, cmd_write
from tkinter import *
import timeit
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#################################################################################
data_size=0;aa=1;end=-1;pkg='';measurement_data=[];vel_out=0;range_out=0;snr_out=0;measurement_count=0;
ser_count=0;ser='fjhk';pause=0;
path = r'E:\Uart_data.txt'
file = open(path, 'w+')
############################################################################
       
def defocus(event):
    event.widget.master.focus_set()
#    event.widget.master.state = 'normal'
#    Port_name.takefocus = False
#    Port_name.state('readonly')
def close(master):
    global end
    if (end == -1):
        file.close()
        master.destroy()
        return
    else:
        end=0
    while 1:
        if (end == 1):
            ser.close()
            file.close()
            master.destroy()
            break

def quit_btn(ser, master):
    global end
    if (end == -1):
        file.close()
        master.destroy()
        return
    while 1:
        if (end == 1):
            ser.close()
            file.close()
            master.destroy()
            break

def go_to_sub(ser, text_out, pkg):
    global aa, end
    ser.reset_input_buffer()
    ser.reset_output_buffer()
#    ser.write(bytes('7e0080401010000', encoding='ascii')) 
    while 1:
        ser.write(bytes.fromhex('55'))
        if (end == 0):
            ser.close()
            break
        break
#    return

    while True:
        data = ser.read(size=17)
        if len(data) > 0:
            print('len= ', len(data))
            print ('Got:', data.hex())
            break

    if (len(data) == 17):
        pkg = cmd_write(data) 
        text_out.config(state=NORMAL)
        text_out.delete(1.0, END)
        text_out.insert(INSERT,pkg[0])
        text_out.insert(INSERT,'\n')
        text_out.insert(INSERT,pkg[1])
        text_out.config(state=DISABLED)
    elif (len(data) == 9):
        pkg = acknowledgment(data)
        text_out.config(state=NORMAL)
        text_out.delete(1.0, END)
        text_out.insert(INSERT,pkg)
        text_out.config(state=DISABLED)
    else:
        pass
    
    return
    
def go_to_start(ser,text_out,l5,):
    global end, line1, figure, x_values, y_values, ax, data_size, snr_out, range_out,vel_out, measurement_count  
    while 1:
        if (end == 0):
            end=1
            break
        data1 = ser.read(size=2)
#        print(data1)
        print(data1.hex())
        if (data1.hex() != 'e007'):
            continue
        else:
            data = ser.read(size=15)
#        starttime = timeit.default_timer()
        if len(data) > 0:
#            print('len= ', len(data))
            data = data1 + data
            print ('Got:', data.hex())
#            print(data)
#            pkg = cmd_write(data) 
            ##############################################
            data_hex =data.hex()
            velocity = data_hex[10:14]
            r = bytearray.fromhex(velocity)
            vel_out = int.from_bytes(r, byteorder='little')
            
            range_out = data_hex[14:18]
            r = bytearray.fromhex(range_out)
            range_out = int.from_bytes(r, byteorder='little')
            
            snr_out = data_hex[18:22]
            r = bytearray.fromhex(snr_out)
            snr_out = int.from_bytes(r, byteorder='little')
            #################################################
            
            
#            text_out.config(state=NORMAL)
#            text_out.delete(1.0, END)
#            text_out.insert(INSERT,f'{vel_out} m/s\n{range_out} m\n{snr_out} dbm')
#            text_out.config(state=DISABLED) 
            
#            file.write(f'{data.hex()}       {vel_out}\n')
            
#            with open(path, 'a+') as file:
#                file.write(f'{vel_out}\n')
            file.write(f'{vel_out}\n')
            
            data_size += len(data)
            l5.config(text=str(data_size))
            
        data=b''
#        print(timeit.default_timer() - starttime)
    return 
        
def go_to_Initialization(Port_name, e1, e2, text_out, *args):
    global end,ser_count, ser,pause
    port_name = Port_name.get()
    bdrate = e1.get()
    bytesize = e2.get()
    port_name_li = port_name.split()
    
    try:
        print(args[1].cget('text'))
        print(ser.isOpen())
    except:
        print(args[0])
        
    ### Below try is to igmore error for command button
    try:
        if (args[1].cget('text') == 'Start'):
            if (ser_count == 0):
                print('done')
                ser = serial.Serial(port=port_name_li[0], baudrate=bdrate, bytesize=int(bytesize), stopbits=1,timeout=1)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser_count = 1
            elif (ser.isOpen() == False):
                ser = serial.Serial(port=port_name_li[0], baudrate=bdrate, bytesize=int(bytesize), stopbits=1,timeout=1)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
            print(ser)
            args[1].configure(text='Pause', background="light green")
            end=2
            t2 = threading.Thread(target=go_to_start, args=(ser,text_out, args[2]))            
            t2.start()
            return
        elif (args[1].cget('text') == 'Pause'):
            end=0
            pause = 1
            args[1].configure(text='Start', background="light sea green")
            return
        elif (args[1].cget('text') == 'Quit'):
            if (ser_count == 0):
                end = -1
            elif (pause == 1):
               end = 1 
            else:
                end = 0
            quit_btn(ser, args[2])
            return 
    except:
        pass
    
    if (ser.isOpen() == True):
        if (args[0] == 'init'):
            pkg = Initialization()
        elif (args[0] == 'tx_power'):
            pkg = tx_power()
        elif (args[0] == 'ld_time'):
            pkg = load_time('read')
        elif (args[0] == 'get_cmd'):
            pkg = get_cmd('read')
        elif (args[0] == 'reset'):
            pkg = reset_cmd('read')
        elif (args[0] == 'fact_res'):
            pkg = factory_reset_cmd('read')
        elif (args[0] == 'data_rate'):
            pkg = data_rate('read')
    print(str(int(len(pkg)/2))+ 'B')
    print(pkg)
    text_out.config(state=NORMAL)
    text_out.delete(1.0, END)
#    text_out.insert(INSERT,pkg)
    text_out.config(state=DISABLED)
    
    if (pkg != ''):            
        t1 = threading.Thread(target=go_to_sub, args=(ser,text_out,pkg,))
        t1.start()
    
 
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
        master.geometry('650x450+250+200')
        master.resizable(0, 0)
        master.title('On Board Computer Stimulator')
        master.iconbitmap(r'E:\spyder_code\New_folder\multipath_test\favicon.ico')
        master.configure(bg='white')
        
        bg_color = 'light Blue'
        
        
        master.protocol("WM_DELETE_WINDOW", partial(close, master))
        
        master_frame = Frame(master, bg='white', width = 640, height=240, bd=1, relief=RIDGE)
        master_frame.grid(row=0, column=0, sticky=N, padx=5, pady=20)
        master_frame.grid_propagate(False)
        
        
        frame0 = Frame(master_frame,  bg='white', width=295, height=20)
        frame0.grid(row=0, column=0, sticky=N, pady=3)
        frame0.grid_propagate(False)
        self.l11 = ttk.Label(frame0, text = "RS422 Port Configuration :",
                font = ("Times New Roman", 12), background='white')
        self.l11.grid(row = 0, column = 0)
        
        frame1 = Frame(master_frame, width=300, bd=3, relief=RIDGE, height=170, bg='light blue')
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
#        self.text.config(state=DISABLED)
        

        self.l1 = ttk.Label(frame1, text = "Baud Rate :",
                font = ("Times New Roman", 10), background=bg_color)
        self.l1.grid(row = 10, column = 0,  padx = 0, pady = 5)
        
        self.e1 = ttk.Entry(frame1, width = 30, foreground='Grey')
        self.e1.insert(10, '921600')
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
        self.Port_name.current(1)
        self.Port_name.grid(row = 20, column = 1) 
        
        self.l3 = ttk.Label(frame1, text = "Byte Size  :",
                font = ("Times New Roman", 10), background=bg_color)
        self.l3.grid(row = 30, column = 0,  padx = 0, pady = 5)
        
        self.e2 = ttk.Entry(frame1, width = 30, foreground='black')
        self.e2.insert(10, '8')
        self.e2.grid(row=30, column=1)
        
        self.l4 = ttk.Label(frame1, text = "Bytes Transfered :",
                font = ("Times New Roman", 10), background=bg_color)
        self.l4.grid(row = 40, column = 0,  padx = 0, pady = 5)
        
        self.l5 = ttk.Label(frame1, text = "0",
                font = ("Times New Roman", 10), background=bg_color)
        self.l5.grid(row = 40, column = 1,  padx = 0, pady = 5 ,sticky=E)
        
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
        
        
        self.b9 = tk.Button(frame1, text='Start',  width=10, background="light sea green")
        self.b9.grid(row=60, column=1,pady=15, padx=10)
        self.b9.configure(command=partial(go_to_Initialization, self.Port_name, 
                                                                  self.e1, self.e2, self.text, self.b9.cget('text'), self.b9, self.l5))
        

        self.b1 = tk.Button(frame1, text='Quit',  width=10, background="red")
        self.b1.grid(row=60, column=0,pady=15, padx=10)
        self.b1.configure(command=partial(go_to_Initialization, self.Port_name, 
                                                                  self.e1, self.e2, self.text, self.b1.cget('text'), self.b1, master))
        
        
        
        
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
