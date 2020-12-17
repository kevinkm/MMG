from machine import UART
from lib.COMMON.Arduino import Arduino_func
from lib.COMMON.timer import Timer
# import uos, time

class MPU6050_JY61P():
    def __init__(self, type=('angle')):
        '''
        EPS32 MODULE
        uart=UART( 1, baudrate=115200, bits=8, parity=None, stop=1, tx=12, rx=14, rts=-1, cts=-1, txbuf=256, rxbuf=256,
              timeout=5000, timeout_char=2 )
        self.uart.init( 115200, bits=8, parity=None, stop=1, pins=(17, 16) )
        # but the 1 may be used as pin9 and pin10, try uart2 first
        uart = UART( 2, baudrate=115200) # for esp32, it is said that uart2 default tx=17,rx=16
        self.uart.init( 115200, bits=8, parity=None, stop=1 )
        '''
        import sys
        s=sys.platform
        if s=='esp8266':
            p=0
        elif s=='esp32': #rx16,tx17
            p=2
        self.getAngle,self.getPalstance,self.getAccel,=0,0,0
        if 'angle' in type:
            self.getAngle=1
        if 'palstance' in type:
            self.getPalstance=1
        if 'accel' in type:
            self.getAccel=1

        self.uart = UART( p, baudrate=115200 )
        self.uart.init( 115200, bits=8, parity=None, stop=1 )
        self.Re_buf = []
        self.angle, self.accel, self.palstance= [], [], []
        self.sum_rx_bytes, self.rx_bytes = b'', b''
        #########################

        self.startLroll = 0
        self.endLroll = 60
        self.startRroll = 359
        self.endRroll = 300

        self.startFrotate = 359
        self.endFrotate = 300
        self.startBrotate = 0
        self.endBrotate = 60

        self.startSpin=0
        self.endSpin=359
        self.RunAfter = Timer.RunAfter

        self.Lrange = range( self.startLroll, self.endLroll + 1 )
        self.Rrange = range( self.endRroll, self.startRroll + 1 )
        self.edge_Lrange = range( self.endLroll, 180 + 1 )
        self.Frange = range( self.endFrotate, self.startFrotate + 1 )
        self.Brange = range( self.startBrotate, self.endBrotate + 1 )
        self.edge_Brange = range( self.endBrotate, 180 + 1 )
        self.Srange= range(self.startSpin,self.endSpin+1)

    def calcGRYO(self, var, basenum):
        for i in range(2, 7, 2):
            var.append(int((int(self.Re_buf[basenum + 1 + i] << 8 | self.Re_buf[basenum+i])) / 32768.0 * 180))

    def current_axis(self):
        while (b'US' not in self.rx_bytes): #UQ=51, US=53
            # if self.RunAfter('g_3000'):
            if self.uart.any():
                self.rx_bytes = self.uart.read()
                self.sum_rx_bytes = self.sum_rx_bytes + self.rx_bytes
                # print (11111)
            # else:
            #     print ('can not get b"UT", so break while ')
            #     break
        if (len(self.sum_rx_bytes))==33:
            # print (22222)
            self.Re_buf, self.angle, self.palstance, self.accel= [], [], [], []
            for i in range( 0, 33 ):
                one_byte = self.sum_rx_bytes[i:i + 1]
                one_int = int.from_bytes( one_byte, "big" )
                self.Re_buf.append( one_int )

            if self.getAccel and self.Re_buf[0] == 0x55 and self.Re_buf[1] == 0x51:
                self.calcGRYO(self.accel, 0)

            if self.getPalstance and self.Re_buf[11] == 0x55 and self.Re_buf[12] == 0x52:
                self.calcGRYO( self.palstance, 11 )

            if self .getAngle and self.Re_buf[22] == 0x55 and self.Re_buf[23] == 0x53:
                self.calcGRYO( self.angle, 22 )

        self.sum_rx_bytes, self.rx_bytes = b'', b''
        return {'accel':self.accel, 'palstance':self.palstance, 'angle': self.angle}

    # function
    def A2(self, angle, range1=0, range2=0, edge_range1=0, startMap1=0, endMap1=0, startMap2=0, endMap2=0, name=0, Maxlevel=10):      #angle2direction
        if angle in range1:
            arduino_map = Arduino_func(startMap1, endMap1, 0, Maxlevel)
            return name[0] + '%02d' % arduino_map.map( angle )
        elif angle in range2:
            arduino_map = Arduino_func(endMap2, startMap2, 0, Maxlevel)
            return name[1] + '%02d' % arduino_map.map( angle, -1 )
        elif angle in edge_range1:
            return name[0] + '10'
        elif angle < endMap2:
            return name[1] + '10'

    def A2D(self, angle, Maxlevel=10):      #angle2direction
        if angle in self.Lrange:
            arduino_map = Arduino_func( self.startLroll, self.endLroll, 0, Maxlevel )
            return 'L' + '%02d' % arduino_map.map( angle )
        elif angle in self.Rrange:
            arduino_map = Arduino_func( self.endRroll, self.startRroll, 0, Maxlevel )
            return 'R' + '%02d' % arduino_map.map( angle, -1 )
        elif angle in self.edge_Lrange:
            return 'L10'
        elif angle < self.endRroll:
            return 'R10'

    def A2M(self, angle, Maxlevel=10):      #angle2move
        if angle in self.Brange:
            arduino_map = Arduino_func( self.startBrotate, self.endBrotate, 0, Maxlevel )
            return 'B' + '%02d' % arduino_map.map( angle )
        elif angle in self.Frange:
            arduino_map = Arduino_func( self.endFrotate, self.startFrotate, 0, Maxlevel )
            return 'F' + '%02d' % arduino_map.map( angle, -1 )
        elif angle in self.edge_Brange:
            return 'B10'
        elif angle < self.endFrotate:
            return 'F10'

    def angleSpin(self,angle, Maxlevel=20):
        if angle in self.Srange:
            arduino_map = Arduino_func( self.startSpin, self.endSpin, 0, Maxlevel )
            return 'S' + '%02d' % arduino_map.map( angle )
        elif angle in self.endSpin:
            return 'S20'

    @property
    def Str_CarDATA(self):
        current_ANGLE = self.current_axis()['angle']
        str1=self.A2(current_ANGLE[0], self.Lrange, self.Rrange, self.edge_Lrange, self.startLroll, self.endLroll, self.startRroll, self.endRroll, 'LR')
        str2=self.A2(current_ANGLE[1], self.Brange, self.Frange, self.edge_Brange, self.startBrotate, self.endBrotate, self.startFrotate, self.endFrotate, 'BF')
        final_str1 = str1 + '-' + str2
        return final_str1

    @property
    def Str_AngleDATA(self):
        # print( self.current_axis )
        a=self.current_axis()['angle']
        # print (a)
        if len(a)==3:
            current_ANGLE = a
            # str1 = self.A2D( current_ANGLE[0] )
            # str2 = self.A2M( current_ANGLE[1] )
            str1 = self.A2( current_ANGLE[0], self.Lrange, self.Rrange, self.edge_Lrange, self.startLroll,
                            self.endLroll, self.startRroll, self.endRroll, 'LR' )
            str2 = self.A2( current_ANGLE[1], self.Brange, self.Frange, self.edge_Brange, self.startBrotate,
                            self.endBrotate, self.startFrotate, self.endFrotate, 'BF' )
            str3 = self.A2( current_ANGLE[2], self.Srange, edge_range1=self.endSpin, startMap1=self.startSpin,
                     endMap1=self.endSpin, name='S', Maxlevel=20 )

            # str3 = self.angleSpin( current_ANGLE[2] )
            final_str1 = str1 + '-' + str2 + '-' + str3
            return final_str1

    # def Decode_CarDATA(self, bytes):
    #     return bytes.decode( "uft-8" ).split( '-' )  # format is: ['Lx/Rx','Fx/Bx']

'''
USAGE:
# HOWTO get the three angles from MPU6050
from GYRO import MPU6050_JY61P
mpu6050=MPU6050_JY61P()
print (mpu6050.current_angle)
>>>[num1,num2,num3]
# HOWTO switch_cli angle to direction or move, format of level is L/Rx, eg.L4 or R6
mpu6050.angle2direction(mpu6050.current_angle[0])
mpu6050.angle2move(mpu6050.current_angle[1])
#ADVANCED USAGE:
#HOW TO use in car 
from GYRO.MPU6050_JY61P import Decode_CarDATA
'''