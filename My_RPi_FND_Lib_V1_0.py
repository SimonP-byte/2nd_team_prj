

'''
  My Rpi FND Lib
  
  Hp    : 010-2402-4398
  Name  : 송 명 규
  Email : mgsong@hanmail.net
  V1.0 == 2024, 07, 07 == 최초작성 

'''


from RPi import GPIO    # GPIO 클레스만 가저옴
from My_Lib import My_STD_Lib_V1_0 as std_7seg
from My_Lib import My_RPi_GPIO_Lib_V1_2 as seg7


fnd_font = (
   #  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   H,   L,   E,   o,   P,  F,
   0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x27,0x7f,0x6f,0x76,0x38,0x79,0x5c,0x73,0x71,
   #  C,    d,    A,    u,    T,    r,   b,  blk
   0x39, 0x5e, 0x77, 0x1c, 0x44, 0x50, 0x7c, 0x00
)
   
# fnd maseg display == 영문 font
__O__  = 0x0d   # o display
__F__  = 0x0f   # F display
__H__  = 0x0a   # H   "
__L__  = 0x0b   # L   "
__E__  = 0x0c   # E   "
__P__  = 0x0e   # P   "
__C__  = 0x10   # C   "
__D__  = 0x11   # d   "
__A__  = 0x12   # A   "
__U__  = 0x13   # u   "
__T__  = 0x14   # t   "
__R__  = 0x15   # r   "
__b__  = 0x16   # b   "
__BLK__  = 0x00   # fnd blk display


# FND Pin Define
#          L1, L2, L3, L4,  A,  B,  C,  D, E, F, G, DP 
FND_Pin = (24, 17, 27, 23, 21, 20, 16, 12, 1, 7, 8, 25)
           
__x1000__ = FND_Pin[0]
__x100__  = FND_Pin[1]
__x10__   = FND_Pin[2]
__x1__    = FND_Pin[3]

__fnd_a__ = FND_Pin[4]
__fnd_b__ = FND_Pin[5]
__fnd_c__ = FND_Pin[6]
__fnd_d__ = FND_Pin[7]
__fnd_e__ = FND_Pin[8]
__fnd_f__ = FND_Pin[9]
__fnd_g__ = FND_Pin[10]
__fnd_dp__ = FND_Pin[11]



fnd_scan = 0
dp_flag = 0

# fnd display func
def fnd_out(data):    
     seg7._d_out_(__fnd_a__, int(data%2))     # bit 0 = lsb
     seg7._d_out_(__fnd_b__, int(data/2%2))   # bit 1 
     seg7._d_out_(__fnd_c__, int(data/4%2))   # bit 2 
     seg7._d_out_(__fnd_d__, int(data/8%2))   # bit 3 
     seg7._d_out_(__fnd_e__, int(data/16%2))  # bit 4  
     seg7._d_out_(__fnd_f__, int(data/32%2))  # bit 5
     seg7._d_out_(__fnd_g__, int(data/64%2))  # bit 6
     seg7._d_out_(__fnd_dp__, int(data/128%2)) # bit 7 = msb


def fnd_dis_A_4(d_buf):    
    global fnd_scan
    fnd_scan = 1 if fnd_scan > 4 else fnd_scan + 1  #3항 연산자
    
    '''
    if fnd_scan > 4:
        fnd_scan = 1
    else:
        fnd_scan = fnd_scan + 1
    '''
    
    match fnd_scan:
        case 1: #x1000
            seg7._d_out_(__x1__, std_7seg.OFF())
            fnd_out(~fnd_font[int(d_buf/1000)]) # data out                       
            seg7._d_out_(__x1000__, std_7seg.ON())
        
        case 2: #x100
            seg7._d_out_(__x1000__, std_7seg.OFF())
            fnd_out(~fnd_font[int(d_buf%1000/100)]) # data out                       
            seg7._d_out_(__x100__, std_7seg.ON())
            
        case 3: #x10
             seg7._d_out_(__x100__, std_7seg.OFF())                  
             fnd_out(~fnd_font[int(d_buf%100/10)]) # data out                                         
             seg7._d_out_(__x10__, std_7seg.ON())
           
        case 4: # x1
             seg7._d_out_(__x10__, std_7seg.OFF())                  
             fnd_out(~fnd_font[int(d_buf%10)]) # data out                                         
             seg7._d_out_(__x1__, std_7seg.ON())     
        
        
    
    















    
    
    