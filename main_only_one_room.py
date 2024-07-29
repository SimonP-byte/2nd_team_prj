
#### sys lib ####
import time as tm
import threading as thrd
import serial

#### prj lib ####
import RPi.GPIO as gpio

#### my lib ####
from package import Rpi_FND_Lib_V1_0 as fnd
from package import My_Rpi_GPIO_Lib_V1_0 as io_lib
from package import My_RPi_I2C_LCD_Lib_V1_0 as lcd_lib
from package.My_STD_Lib_V1_0 import *


port = "/dev/ttyAMA3"
baud = 9600
ser = serial.Serial("/dev/ttyAMA3", 9600, timeout = 0.1)

ser.close()
ser.open()

cnt = 1234
rx_flag = 0
alarm_flag = 0

NOA = 0 # Number of arduino

# for thread
fnd_buf = 0
loop_ = 0

def fnd_thread():
    global loop_
    global alarm_flag
    global fnd_buf
    global NOA
    
    if alarm_flag == 1:
        tm.sleep(0.0001)
        loop_ = loop_ + 1
        if(loop_>500):
            loop_ = 0
            if NOA == 0:
                fnd_buf = 1111  # room 1 warning
                
            elif NOA == 1:
                fnd_buf = 2222 # room 2 warning
                
    elif alarm_flag == 0: #safe
        tm.sleep(0.0001)
        loop_ = loop_ + 1
        if(loop_>500):
            loop_ = 0
            if NOA == 0:
                fnd_buf = 1000  # room 1 safe
                #fnd.fnd_dis_A_4(fnd_buf)
            elif NOA == 1:
                fnd_buf = 2000 # room 2 safe
    
           
    FND_thread = thrd.Thread(target = fnd_thread)
    FND_thread.start()
            
def dis_fnd_thread():
    global fnd_buf
    fnd.fnd_dis_A_4(fnd_buf)
    
    DIS_FND_thread = thrd.Thread(target = dis_fnd_thread)
    DIS_FND_thread.start()

def timer_thrd():
    #print("thrd func...")
    
    if ser_2.readable():
        response = ser_2.readline()
        #print(response)
    
    thread_1 = thrd.Timer(0.2, timer_thrd)
    thread_1.start()
              

def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.cleanup()
    
       
#     for i in io_lib.LED_Pin:
#         gpio.setup(i, gpio.OUT)
#     for k in seg7.FND_Pin:
#         gpio.setup(k, gpio.OUT)
    
    gpio.setup(6, gpio.OUT)
    io_lib._d_out_(6, 0)
    gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)
    
    # FND
    for i in fnd.FND_Pin:
        gpio.setup(i, gpio.OUT)
        
    FND_thread = thrd.Thread(target = fnd_thread)
    FND_thread.start()
    
    DIS_FND_thread = thrd.Thread(target = dis_fnd_thread)
    DIS_FND_thread.start()
    
#     thread_1 = thrd.Timer(0.2, timer_thrd)
#     thread_1.start()

def main():
    setup()
    try:
        while True:
            global rx_flag
            global NOA
            global AN, error
            global alarm_flag
            
            if io_lib._d_in_(21) == 0:
                alarm_flag = 0
            
            if rx_flag == 0:
                io_lib._d_out_(6, 1)
                
                if NOA == 0:
                    if alarm_flag == 0:
                        ser.write(b"S00100\n")
                    elif alarm_flag == 1:
                        ser.write(b"S00101\n")
                        
                elif NOA == 1:
                    if alarm_flag == 0:
                        ser.write(b"S00200\n")
                    elif alarm_flag == 1:
                        ser.write(b"S00201\n")
                
                NOA += 1
                if NOA > 1:
                    NOA = 0
                    
                tm.sleep(0.01)
                io_lib._d_out_(6, 0)
                rx_flag = 1
                
            tm.sleep(0.3)
            
            if rx_flag == 1 & ser.readable():
                rx_buf = ser.readline()
                #print(rx_buf)
                if len(rx_buf) >= 6:
                    if rx_buf[4] == 48:	# 48 == '0'
                        if rx_buf[5] == 48: # 48 == '0'
                            rx_flag = 0
                            alarm_flag = 0
                        elif rx_buf[5] == 49: # 49 == '1'
                            rx_flag = 0
                            alarm_flag = 1
                else :	
                    rx_flag = 0
                    
            tm.sleep(0.3)
            
    except KeyboardInterrupt:
        print("Ctrl + c KeyboardInterrupt")        
    finally:
        pass
        
#===============================================================

# Program Strat main
if __name__ == "__main__":
    main()
