from machine import PWM,Pin
from lib.COMMON.Arduino import Arduino_func

class MD_TB6612FNG():
    # d6-gpio12, d7-gpio13 for motorA, d2-gpio4 as PWMA
    # d5-gpio14, d8-gpio15 for motorB. NO SUFFICIENT GPIO, use PWMA.
    def __init__(self, in1=12, in2=13, in3=14, in4=15, pwm=4, type='Single', Min_Level=0, Max_Level=10, Min_duty=0,
                 Max_duty=1023):
        self.DOUBLEMOTOR = False
        self.DOUBLEMOTOR_DIRECTIONAL = False
        self.PWMA = PWM( Pin( pwm ), freq=50 )
        self.MOTORA = {'out1': Pin( in1, Pin.OUT ), 'out2': Pin( in2, Pin.OUT )}
        self.Min_Move_Level = Min_Level
        self.Max_Move_Level = Max_Level
        self.Min_DUTY = Min_duty
        self.Max_DUTY = Max_duty
        if 'Double' in type:
            if type == 'Double_directional':
                self.DOUBLEMOTOR = True
            else:
                self.DOUBLEMOTOR_DIRECTIONAL = True
            self.MOTORB = {'out1': Pin( in3, Pin.OUT ), 'out2': Pin( in4, Pin.OUT )}
            # self.motor = self.servo.duty( 500 )

    def motorSpin(self, motor,num):
        if num == 1:
            motor['out1'].value( 1 )
            motor['out2'].value( 0 )
        elif num == 0:
            motor['out1'].value( 0 )
            motor['out2'].value( 1 )

    def forward(self, value):
        self.PWMA.duty( value )
        self.motorSpin( self.MOTORA,1 )

        if self.DOUBLEMOTOR:
            self.motorSpin(self.MOTORB, 1 )

    def backward(self, value):
        self.PWMA.duty( value )
        self.motorSpin(self.MOTORA, 0 )

        if self.DOUBLEMOTOR:
            self.motorSpin(self.MOTORB, 0 )

    # ONLY FOR DOUBLE MOTORS, motorA = left side wheels, motorB = right side wheels
    def motor_turnleft(self, value):
        self.PWMA.duty( value )
        if self.DOUBLEMOTOR_DIRECTIONAL:
            self.motorSpin(self.MOTORA, 0 )
            self.motorSpin(self.MOTORB, 1 )

    def motor_turnright(self, value):
        self.PWMA.duty( value )
        if self.DOUBLEMOTOR_DIRECTIONAL:
            self.motorSpin(self.MOTORA, 1 )
            self.motorSpin(self.MOTORB, 0 )

    def move(self, value):
        move_value = list( value )
        move_value.pop( 0 )
        move_value = int( ''.join( move_value ) )
        if value[0] == 'F':
            arduino_map = Arduino_func( self.Min_Move_Level, self.Max_Move_Level, self.Min_DUTY, self.Max_DUTY )
            move_value = arduino_map.map( move_value )
            self.forward( move_value )
        elif value[0] == 'B':
            arduino_map = Arduino_func( self.Min_Move_Level, self.Max_Move_Level, self.Min_DUTY, self.Max_DUTY )
            move_value = arduino_map.map( move_value )
            self.backward( move_value )
        # print('move_value' + str(move_value))