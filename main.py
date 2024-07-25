
#### sys lib ####
import time as tm
import threading as thrd
import serial

#### prj lib ####
import RPi.GPIO as gpio

#### my lib ####
from package import Rpi_FND_Lib_V1_0 as seg7
from package import My_Rpi_GPIO_Lib_V1_0 as io_lib

 #          L1, L2, L3, L4,  A,  B,  C,  D, E, F, G, DP 
FND1_Pin = [12, 16, 20, 21, 9, 11, 0, 5, 6, 13, 19, 26]
FND2_Pin = [12, 16, 20, 21, 9, 11, 0, 5, 6, 13, 19, 26]

FND_1 = seg7.FND_()
FND_2 = seg7.FND_()
FND_1.FND_init_(FND1_Pin)
FND_2.FND_init_(FND2_Pin)


def FND_cal():
    
    tm.sleep(0.2)
    thread_1 = thrd.Thread(target=FND_cal)
    thread_1.start()
    
def LED_dis():
    
    tm.sleep(0.2)
    thread_2 = thrd.Thread(target=LED_dis)
    thread_2.start()
    

def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    
    for i in io_lib.LED_Pin:
        gpio.setup(i, gpio.OUT)
    for k in FND_1.FND_Pin:
        gpio.setup(k, gpio.OUT)
    
    thread_1 = thrd.Thread(target=FND_cal)
    thread_1.start()
    
    thread_2 = thrd.Thread(target=LED_dis)
    thread_2.start()
    
def main():
    setup()
    try:
        while True:
            
            pass
                
    except KeyboardInterrupt:
        print("Ctrl + c KeyboardInterrupt")        
    finally:
        pass
        
#===============================================================

# Program Strat main
if __name__ == "__main__":
    main()