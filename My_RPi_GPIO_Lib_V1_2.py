
'''
  My RPi.GPIO 전용 Lib
  
  Hp    : 010-2402-4398
  Name  : 송 명 규
  Email : mgsong@hanmail.net
  V1.0 == 2024, 07, 03 == 최초작성
  V1.2 == 2024, 07, 13 == 라이브러리 분리하여 RPi.GPIO 전용 Lib로 작성 함 
'''

from RPi import GPIO    
from My_Lib import My_STD_Lib_V1_0 as std



# LED PIN
LED_Pin = (10,9,11,5,6,13,19,26)

__LED_0__ = LED_Pin[0]
__LED_1__ = LED_Pin[1]
__LED_2__ = LED_Pin[2]
__LED_3__ = LED_Pin[3]
__LED_4__ = LED_Pin[4]
__LED_5__ = LED_Pin[5]
__LED_6__ = LED_Pin[6]
__LED_7__ = LED_Pin[7]


# SW Pin Define
SW_Pin = (4, 22, 18, 15)

# SW Pin Define
__SW1__ = SW_Pin[0]
__SW2__ = SW_Pin[1]
__SW3__ = SW_Pin[2]
__SW4__ = SW_Pin[3]


def pin_func(pin):
    print(f"GPIO Pin Func = {str(GPIO.gpio_function(pin))}")


'''      
def gpio_help():
    print(GPIO.RPI_INFO())
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
        pin_out(LED_Pin[k], not (data >> k) % 2)    
#======================================================

#GPIO PIN Control Class
#Class        
class Gpio_Lib_Pin_Out:
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
        


    