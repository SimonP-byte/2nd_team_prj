

# Python Rpi GPIO LIB
from RPi import GPIO

#system lib
import time as tm
import threading

# My Lib == Default package Type Load
from LIB import * 
from LIB import My_Rpi_GPIO_Lib_V1_0
from LIB.My_Rpi_GPIO_Lib_V1_0 import Gpio_Pin_Out
from LIB import My_Rpi_FND_Lib_V1_0 as fnd

#sub func



#=====================================================================

# Global variable


fnd_buf = 0
alarm_flag = 0
loop_ = 0
#loop_2 = 0
NOA = 0
#flag = 0
#class set
io = Gpio_Pin_Out()
#====================================================================
# system sub Func
def fnd_thread():
    global loop_
    global alarm_flag
    global fnd_buf
    global NOA
    
    
    
    if alarm_flag == 1:
        tm.sleep(0.0001)
        loop_ = loop_ + 1
        if(loop_>20000):
            loop_ = 0
            if NOA == 0:
                fnd_buf = 1111  # room 1 warning
                
            elif NOA == 1:
                fnd_buf = 2222 # room 2 warning
                
    elif alarm_flag == 0: #safe
        tm.sleep(0.0001)
        loop_ = loop_ + 1
        if(loop_>20000):
            loop_ = 0
            if NOA == 0:
                fnd_buf = 1000  # room 1 safe
                #fnd.fnd_dis_A_4(fnd_buf)
            elif NOA == 1:
                fnd_buf = 2000 # room 2 safe
    
           
    FND_thread = threading.Thread(target = fnd_thread)
    FND_thread.start()
            
def dis_fnd_thread():
    global fnd_buf
    fnd.fnd_dis_A_4(fnd_buf)
    
    DIS_FND_thread = threading.Thread(target = dis_fnd_thread)
    DIS_FND_thread.start()
                    
    
def setup():
    # GPIO Lib Set
    GPIO.setwarnings(False)
    # gpio Mode Set
    GPIO.setmode(GPIO.BCM) #BOARD
    
    
    
    #Dev GPIO Pin Set
    # 1 LED
    for i in My_Rpi_GPIO_Lib_V1_0.LED_Pin:
        GPIO.setup(i, GPIO.OUT)
    # 2 FND
    for i in fnd.FND_Pin:
        GPIO.setup(i, GPIO.OUT)
    # 3 print Consol out Set   
    print("\x1b[32m")   #text colorprint
    #print("\x1b[45m");  // back Color
    
    #system set
    
    #threading set
    FND_thread = threading.Thread(target = fnd_thread)
    FND_thread.start()
    
    DIS_FND_thread = threading.Thread(target = dis_fnd_thread)
    DIS_FND_thread.start()
#================================================================
# system main func
def main():
    setup()
    global warning_flag
    global NOA
    
    try:
        
        #cnt = 1234
        while True:
            '''
            global fnd_buf
            global flag
            global loop_2
            
            loop_2 += 1
            if loop_2 > 800 :
                loop_2 = 0
                if flag == 1:
                    flag=0
                else:
                    flag = 1
            
            if flag == 0:
                alarm_flag = 0
                NOA = 0
                #tm.sleep(3)
                #flag = 1
            elif flag == 1:
                alarm_flag = 1
                NOA = 1
                #tm.sleep(3)
                #flag = 0
            #print(flag)
            #print(loop_2)
            #fnd.fnd_dis_A_4(fnd_buf)
            #tm.sleep(0.0001)
            '''
            
            
        '''
            tm.sleep(0.001)  #1
            t_loop +=  1     #2
            if t_loop > 200: #3
                t_loop = 0   #4
                cnt += 1     #5
                if cnt > 5000: #6
                    cnt = 0   #7
            fnd.fnd_dis_A_4(cnt) #8      
        '''
        
    except KeyboardInterrupt:
        print("Ctrl + c KeyboardInterrupt")
            
   
        
    finally:
        GPIO.cleanup()
        print("GPIO Close")
#==================================================================        
                
# Program Strat main
if __name__ == "__main__":
    main()
    
    

