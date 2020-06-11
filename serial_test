import serial
import tkinter as tk 
from tkinter import ttk 
import serial.tools.list_ports
from time import sleep
import threading

port_list=[];
ports = list(serial.tools.list_ports.comports())
for p in ports:
    port_list.append(p)
port_list = tuple(port_list)

def callback_baud(input, num_check):
    if input.isdigit():
        if (input == '0'):
            e1.config(foreground='black')
        ###############################################
        if (num_check.isdigit() == False):
            err_msg.grid(row=0, column=1, padx=15)
            err_msg.config(text='Please enter a number')
            return False
        else:
            err_msg.grid_forget()
#            err_msg.config(text='')
        ##############################################
    return True

def callback_port(input):
    if (input != 'Select Port name'):
        pass
#        Port_name.config(foreground='black', state='disabled')
#        Port_name.config(foreground='black', state='normal')
    return True

def defocus(event):
    event.widget.master.focus_set()
#    event.widget.master.state = 'normal'
#    Port_name.takefocus = False
#    Port_name.state('readonly')
    

def go_to_sub():
    port_name = Port_name.get()
    bdrate = e1.get()
    bytesize = e2.get()
    port_name_li = port_name.split()
    print(bdrate)
    print(port_name)
    print(bytesize)
    ser = serial.Serial(port=port_name_li[0], baudrate=bdrate, bytesize=serial.EIGHTBITS, 
                        stopbits=1)
#    print(ser.read(1)) 
#    ser.open()
    print(ser.isOpen())
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    

#    ser.write(bytes(bytesize, encoding='utf-8'))   ##### TO write
    while True:
        #cmd = raw_input("Enter command or 'exit':")
            # for Python 2
        cmd = input("Enter command or 'exit':")
            # for Python 3
        if cmd == 'e':
            ser.close()
            return 
        else:
#            ser.write(b'NAGENDRA')
            out = ser.read(size=int(bytesize))
            print(out)
#    while 1:
#        data = bytearray(b'Hello')
#        print(data)
#        No = ser.write(data)
#        sleep(1)
#    print(No)
#    while True:
#        data = ser.read(9999)
#        if len(data) > 0:
#            print ('Got:', data)
#    
#        sleep(0.5)
#        print ('not blocked' )
    ser.close()
    
    print(ser.isOpen())

def quit_btn():
    master.destroy()

master = tk.Tk() 
master.geometry('450x200')
master.resizable(0, 0)
master.title('OBC GUI')
master.iconbitmap(r'E:\spyder_code\New_folder\multipath_test\favicon.ico')

l1 = ttk.Label(master, text = "Baudrate :",  
        font = ("Times New Roman", 10))
l1.grid(row = 10, column = 0,  padx = 0, pady = 5)

e1 = ttk.Entry(width = 38, foreground='Grey')
e1.insert(10, '9600')
e1.grid(row= 10, column=1)

reg = master.register(callback_baud)
e1.config(validate ="all",  
         validatecommand =(reg, '%i', '%S'))

err_msg = ttk.Label(master, font = ("Times New Roman", 10), foreground='red')

l2 = ttk.Label(master, text = "Port Name :",  
        font = ("Times New Roman", 10))
l2.grid(row = 20, column = 0,  padx = 10, pady = 5) 
#
n = tk.StringVar() 
Port_name = ttk.Combobox(master, width = 35, textvariable = n, foreground='Grey', state='readonly')
Port_name.set('Select Port name')
Port_name['values'] = port_list
Port_name.bind("<FocusIn>", defocus)
Port_name.current(0)
Port_name.grid(row = 20, column = 1) 

#reg2 = master.register(callback_port)
#Port_name.config(validate ="all",  
#         validatecommand =(reg2, '%P'))

l3 = ttk.Label(master, text = "Byte Size  :",  
        font = ("Times New Roman", 10))
l3.grid(row = 30, column = 0,  padx = 0, pady = 5)

e2 = ttk.Entry(width = 38, foreground='black')
e2.insert(10, '2')
e2.grid(row=30, column=1)

b1 = tk.Button(master, text='Submit', command=go_to_sub, background="light green")
b1.grid(row=40, column=2,pady=15)
b2 = tk.Button(master, text='Quit', command=quit_btn, background="red")
b2.grid(row=40, column=0,pady=15)

master.mainloop()
