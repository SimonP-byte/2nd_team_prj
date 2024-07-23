

# LED define

import RPi.GPIO as GPIO



def ON():
    return 1
def OFF():
    return 0

__ON__  =  0
__OFF__ =  1


# LED Pin define
LED_Pin = [14,15,18,23,24,25,8,7]

__LED_0__ = LED_Pin[0]
__LED_1__ = LED_Pin[1]
__LED_2__ = LED_Pin[2]
__LED_3__ = LED_Pin[3]
__LED_4__ = LED_Pin[4]
__LED_5__ = LED_Pin[5]
__LED_6__ = LED_Pin[6]
__LED_7__ = LED_Pin[7]


'''
__LED0__ = 10

def LED7():
    return 26
'''


def _d_out_(pin, value):
    GPIO.output(pin, value)
    
def _pin_out_(pin, value):
    GPIO.output(pin, value)    
    
def _d_in_(pin):
    return  GPIO.input(pin)
    
def _pin_set_(pin):
    GPIO.output(pin, GPIO.HIGH)
    
def _pin_clr_(pin):     
    GPIO.output(pin, GPIO.LOW)
    
def _pin_tg_(pin):
    GPIO.output(pin, not d_in(pin))
    
def _pin_chk_(pin):
    return _d_in_(pin)
    
def _byte_out_(data):
    for k in range(0, 8):        
        _pin_out_(LED_Pin[k], not (data >> k) % 2)
        
def _m_map_(ptr, in_min, in_max, out_min, out_max):
    return int(((ptr - in_min) * (out_max - out_min)) / ((in_max - in_min) + out_min)) 
#======================================================

#GPIO PIN Control Class
#Class        
class Gpio_Pin_Out:
    def __init__(self):
        self.buf = 0
        #pass 
    def d_out(self, pin, value):
        GPIO.output(pin, value)
    
    def pin_out(self, pin, value):
        GPIO.output(pin, value)    
    
    def d_in(self, pin):
        return  GPIO.input(pin)
    
    def pin_set(self, pin):
        GPIO.output(pin, GPIO.HIGH)
    
    def pin_clr(self, pin):     
        GPIO.output(pin, GPIO.LOW)
    
    def pin_tg(self, pin):
        GPIO.output(pin, not self.d_in(pin))
    
    def pin_chk(self, pin):
        return self.d_in(pin)
    
    def byte_out(self, data):
        for k in range(0, 8):        
            self.pin_out(LED_Pin[k], not (data >> k) % 2)
            
    def m_map(self, ptr, in_min, in_max, out_min, out_max):
        return int(((ptr - in_min) * (out_max - out_min)) / ((in_max - in_min) + out_min))         
