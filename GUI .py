from serial import *
from Tkinter import *
import time
import serial.tools.list_ports
import csv
master = Tk()
import datetime
master.wm_title("Reading Serial")
#check=0
baudRate = 460800
ser='None'
comport='None'
buffer=[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#===============================
def connect():
    global comport
    comport=variable.get()
    global ser
    ser = Serial(comport , baudRate, timeout=0, writeTimeout=0)
#============================
comlist =list(serial.tools.list_ports.comports())
connected = []
for element in comlist:
    connected.append(element.device)
variable = StringVar(master)
def readSerial():
    #global file
    global writer1
    #writer = csv.writer(file)
    #global writer
    while True:
        c = ser.read() # attempt to read a character from Serial           
        #was anything read?
        if len(c) == 0:
            break                  
            # get the buffer from outside of this function
        global serBuffer                 
        # check if character is a delimeter
        if c == '\r':
            c = '' # don't want returns. chuck it
                                    
        if c == '\n':
            #serBuffer += "\n" # add the newline to the buffer
            #print serBuffer
            #add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            log.insert('0.0', "\n") 
            if serBuffer.find(':')>0:
                name,value=serBuffer.split(':',1)
                currentDT = str(datetime.datetime.now())
                writer1.writerow([currentDT,name,value])
            serBuffer = "" # empty the buffer
        else:
            serBuffer += c # add to the buffer                    
    master.after(10, readSerial) # check serial again soon            
                

#===============================================================================

def disconnect():
    global comport
    #Serial(comport , baudRate, timeout=0, writeTimeout=0).close()
    ser.close()
    print (ser.is_open)

def stop(): #This is for stop logging the data. not implemented yet 
    u=0

def start():
    buffer1=[str(item) for item in buffer]
    print buffer1
    ser.write(buffer1)
    #global file
    global writer1
    #file = open('text.txt', 'wb')
    #writer = csv.writer(file)
    #writer = writer(file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #writer = csv.writer(open('data.csv', 'wb'), delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer1 = csv.writer(open('data.csv', 'w'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer1.writerow(["TimeStamp","Name","Value"])
    master.after(100, readSerial)

def datalog():
    master.after(100, readSerial1)
def destroy1():
    global file
    file.close()
    master.destroy 

option = OptionMenu(master, variable,*connected).grid(row=0,column=0)
Button(master, text="connect", command=connect).grid(row=0, column=1, padx=10, pady=10)  # TO open the port
Button(master, text="start", command=start).grid(row=0, column=3,sticky=W,padx=10, pady=10)
Button(master, text="stop",command=stop).grid(row=0, column=4,padx=10, pady=10)
Button(master, text="disconnect", command=disconnect).grid(row=0, column=2, padx=10, pady=10) # To close the port
Button(master, text="Exit",command=destroy1).grid(row=0, column=8, padx=10, pady=10) # Button to exit the window
#Button(master, text="DataLog",command=datalog).grid(row=0, column=6, padx=10, pady=10) # Button to exit the window
#ser.write(buffer)
#make a TkInter Window
# make a scrollbar
scrollbar = Scrollbar(master)
scrollbar.grid(row=1,column=13)
# make a text box to put the serial output
log = Text ( master, width=20, height=6, takefocus=0)
log.grid(row=1,column=9)

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)

#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
serBuffer = ""


# after initializing serial, an arduino may need a bit of time to reset

Button(master, text="connect", command=connect).grid(row=0, column=1, padx=10, pady=10) # To close the port
#Button(root, text="disconnect", command=disconnect).pack()
#root.after(100, readSerial)

#=========================================================================

Label(master, text="Temperature").grid(row=3, column=0,sticky=W,padx=5, pady=5)
var1 =IntVar()
def sett1(): # assign check button status in first index of buffer
    buffer[1]=var1.get()    
chk1 = Checkbutton(master, variable=var1,command=sett1).grid(row=3, column=1,sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=4, column=0,sticky=W,padx=5, pady=5)
variable1 = StringVar(master)
variable1.set("1")
def set1():
    if variable1.get()=="1":
        buffer[2]=1
    elif variable1.get()=="7":
        buffer[2]=2 
    elif variable1.get()=="12.5":   
        buffer[2]=3 
option1 = OptionMenu(master, variable1,"1","7","12.5").grid(row=4,column=1,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set1).grid(row=4, column=2,sticky=W,padx=5, pady=5)

#======================================================================== HUMIDITY

Label(master, text="Humidity").grid(row=3, column=5,sticky=W,padx=5, pady=5)
def sett2():
    buffer[3]=var2.get()
var2 = IntVar()
chk2 = Checkbutton(master, variable=var2,command=sett2).grid(row=3, column=6,sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=4, column=5,sticky=W,padx=5, pady=5)
variable2 = StringVar(master)
variable2.set("1")
def set2():
    if variable2.get()=="1":
        buffer[4]=1
    elif variable2.get()=="7":
        buffer[4]=2 
    elif variable2.get()=="12.5":   
        buffer[4]=3 
    else:
        buffer[4]=4
option2 = OptionMenu(master, variable2,"1","7","12.5","25").grid(row=4,column=6,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set2).grid(row=4, column=7, sticky=W,padx=5, pady=5)

#===============================================================================PRESSURE

Label(master, text="Pressure").grid(row=6, column=0,sticky=W,padx=5, pady=5)
def sett3():
    buffer[5]=var3.get()
var3 = IntVar()
chk3 = Checkbutton(master, variable=var3,command=sett3).grid(row=6, column=1,sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=7, column=0,sticky=W,padx=5, pady=5)
variable3 = StringVar(master)
variable3.set("1")
def set3():
    if variable3.get()=="1":
        buffer[6]=1
    elif variable3.get()=="7":
        buffer[6]=2 
    elif variable3.get()=="12.5":   
        buffer[6]=3 
    else:
        buffer[4]=4
option3 = OptionMenu(master, variable3,"1","7","12.5","25").grid(row=7,column=1,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set3).grid(row=7, column=2, sticky=W,padx=5, pady=5)

#==============================================================================ACCELEROMETER

Label(master, text="Accelerometer").grid(row=6, column=5,sticky=W,padx=5, pady=5)
def sett4():
    buffer[7]=var4.get()
var4 = IntVar()
chk4 = Checkbutton(master, variable=var4,command=sett4).grid(row=6, column=6, sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=7, column=5,sticky=W,padx=5, pady=5)
variable4 = StringVar(master)
variable4.set("10")
def set4():
    if variable4.get()=="10":
        buffer[8]=1
    elif variable4.get()=="50":
        buffer[8]=2 
    elif variable4.get()=="119":    
        buffer[8]=3 
    elif variable4.get()=="238":
        buffer[8]=4
    elif variable4.get()=="476":
        buffer[8]=5
    else:
        buffer[8]=6
option4 = OptionMenu(master, variable4,"10","50","119","238","476","952").grid(row=7,column=6,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set4).grid(row=7, column=7, sticky=W,padx=5, pady=5)
Label(master, text="FullScale").grid(row=8, column=5,sticky=W,padx=5, pady=5)
value1 = StringVar(master)
value1.set("2")
def set5():
    if value1.get()=="2":
        buffer[9]=1
    elif value1.get()=="4":
        buffer[9]=2 
    elif value1.get()=="8": 
        buffer[9]=3 
    else:
        buffer[9]=4
opt1 = OptionMenu(master, value1,"2","4","8","16").grid(row=8,column=6,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set5).grid(row=8, column=7, sticky=W,padx=5, pady=5)

#===============================================================================================GYROMETER

Label(master, text="Gyrometer").grid(row=10, column=0,sticky=W,padx=5, pady=5)
def sett5():
    buffer[10]=var5.get()
var5 = IntVar()
chk5 = Checkbutton(master, variable=var5,command=sett5).grid(row=10, column=1,sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=11, column=0,sticky=W,padx=5, pady=5)
variable5 = StringVar(master)
variable5.set("15")
def set6():
    if variable5.get()=="15":
        buffer[11]=1
    elif variable5.get()=="50":
        buffer[11]=2    
    elif variable5.get()=="119":    
        buffer[11]=3    
    elif variable5.get()=="238":
        buffer[11]=4
    elif variable5.get()=="476":
        buffer[11]=5
    else:
        buffer[11]=6
option5 = OptionMenu(master, variable5,"15","60","119","238","476","952").grid(row=11,column=1,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set6).grid(row=11, column=2, sticky=W,padx=5, pady=5)
Label(master, text="FullScale").grid(row=12, column=0,sticky=W,padx=5, pady=5)
value2 = StringVar(master)
value2.set("245")
def set7():
    if value2.get()=="245":
        buffer[12]=1
    elif value2.get()=="500":
        buffer[12]=2        
    else:
        buffer[12]=3
opt2 = OptionMenu(master, value2,"245","500","2000").grid(row=12,column=1,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set7).grid(row=12, column=2, sticky=W,padx=5, pady=5)

#===============================================================================================MAGNETOMETER

Label(master, text="Magnetometer").grid(row=10, column=5,sticky=W,padx=5, pady=5)
def sett6():
    buffer[13]=var6.get()
var6 = IntVar()
chk6 = Checkbutton(master,variable=var6,command=sett6).grid(row=10, column=6, sticky=W,padx=5, pady=5)
Label(master, text="ODR").grid(row=11, column=5,sticky=W,padx=5, pady=5)
variable6 = StringVar(master)
variable6.set("0.625")
def set8():
    if variable6.get()=="0.625":
        buffer[14]=1
    elif variable6.get()=="1.25":
        buffer[14]=2    
    elif variable6.get()=="2.5":    
        buffer[14]=3    
    elif variable6.get()=="5":
        buffer[14]=4
    elif variable6.get()=="10":
        buffer[14]=5
    elif variable6.get()=="20":
        buffer[14]=6
    elif variable6.get()=="40":
        buffer[14]=7
    else:
        buffer[14]='8'
option6 = OptionMenu(master, variable6,"0.625","1.25","2.5","5","10","20","40","80").grid(row=11,column=6,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set8).grid(row=11, column=7, sticky=W,padx=5, pady=5)
Label(master, text="FullScale").grid(row=12, column=5,sticky=W,padx=5, pady=5)
value3 = StringVar(master)
value3.set("4")
def set9():
    if value3.get()=="4":
        buffer[15]=1
    elif value3.get()=="8":
        buffer[15]=2    
    elif value3.get()=="12":
        buffer[15]=3    
    else:
        buffer[15]=4
opt3 = OptionMenu(master, value3,"4","8","12","16").grid(row=12,column=6,sticky=W,padx=5, pady=5)
Button(master, text='Set', command=set9).grid(row=12, column=7,sticky=W,padx=5, pady=5)

#===========================================================================
master.mainloop()