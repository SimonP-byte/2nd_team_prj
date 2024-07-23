

from RPi import GPIO
from package import My_Rpi_GPIO_Lib_V1_0 as seg7

fnd_font = (
   #  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   H,   L,   E,   o,   P,  F,
   0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x27,0x7f,0x6f,0x76,0x38,0x79,0x5c,0x73,0x71,
   #  C,    d,    A,    u,    T,    r,   b,  blk
   0x39, 0x5e, 0x77, 0x1c, 0x44, 0x50, 0x7c, 0x00
)
   
# fnd maseg display
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
FND_Pin = (12, 16, 20, 21, 9, 11, 0, 5, 6, 13, 19, 26)
           
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

# FND Pin Define
 #          L1, L2, L3, L4,  A,  B,  C,  D, E, F, G, DP 
FND1_Pin = (12, 16, 20, 21, 9, 11, 0, 5, 6, 13, 19, 26)
 #          L1, L2, L3, L4,  A,  B,  C,  D, E, F, G, DP 
FND2_Pin = (12, 16, 20, 21, 9, 11, 0, 5, 6, 13, 19, 26)

fnd_scan = 0

class FND_:
    
    fnd_font = (
       #  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   H,   L,   E,   o,   P,  F,
       0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x27,0x7f,0x6f,0x76,0x38,0x79,0x5c,0x73,0x71,
       #  C,    d,    A,    u,    T,    r,   b,  blk
       0x39, 0x5e, 0x77, 0x1c, 0x44, 0x50, 0x7c, 0x00
    )
       
    # fnd maseg display
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
    
    def FND_init_(self, data):
        self.FND_Pin = data
        
        self.__x1000__ = FND_Pin[0]
        self.__x100__  = FND_Pin[1]
        self.__x10__   = FND_Pin[2]
        self.__x1__    = FND_Pin[3]

        self.__fnd_a__ = FND_Pin[4]
        self.__fnd_b__ = FND_Pin[5]
        self.__fnd_c__ = FND_Pin[6]
        self.__fnd_d__ = FND_Pin[7]
        self.__fnd_e__ = FND_Pin[8]
        self.__fnd_f__ = FND_Pin[9]
        self.__fnd_g__ = FND_Pin[10]
        self.__fnd_dp__ = FND_Pin[11]
        
        self.fnd_scan = 0


    # fnd display func
    def fnd_out(self, data):    
         seg7._d_out_(__fnd_a__, int(data%2))     # bit 0 = lsb
         seg7._d_out_(__fnd_b__, int(data/2%2))   # bit 1 
         seg7._d_out_(__fnd_c__, int(data/4%2))   # bit 2 
         seg7._d_out_(__fnd_d__, int(data/8%2))   # bit 3 
         seg7._d_out_(__fnd_e__, int(data/16%2))  # bit 4  
         seg7._d_out_(__fnd_f__, int(data/32%2))  # bit 5
         seg7._d_out_(__fnd_g__, int(data/64%2))  # bit 6
         seg7._d_out_(__fnd_dp__, int(data/128%2)) # bit 7 = msb


    def fnd_dis_A_4(self, data):    
        self.d_buf = data
        self.fnd_scan = 1 if self.fnd_scan > 4 else self.fnd_scan + 1
        
        match self.fnd_scan:
            case 1: #x1000
                seg7._d_out_(self.__x1__, seg7.OFF())
                self.fnd_out(~fnd_font[int(self.d_buf/1000)]) # data out                       
                seg7._d_out_(self.__x1000__, seg7.ON())
            
            case 2: #x100
                seg7._d_out_(__x1000__, seg7.OFF())
                self.fnd_out(~fnd_font[int(self.d_buf%1000/100)]) # data out                       
                seg7._d_out_(__x100__, seg7.ON())
                
            case 3: #x10
                 seg7._d_out_(__x100__, seg7.OFF())                  
                 self.fnd_out(~fnd_font[int(self.d_buf%100/10)]) # data out                                         
                 seg7._d_out_(__x10__, seg7.ON())
               
            case 4: # x1
                 seg7._d_out_(__x10__, seg7.OFF())
                 self.fnd_out(~fnd_font[int(self.d_buf%10)]) # data out           
                 seg7._d_out_(__x1__, seg7.ON())
