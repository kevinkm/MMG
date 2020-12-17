from machine import PWM,Pin
from lib.COMMON.Arduino import Arduino_func


class MD_L298N():
    # d6-gpio12, d7-gpio13 for motorA,
    # d5-gpio14, d8-gpio15 for motorB.
    def __init__(self, IO1=12, IO2=13, IO3=14, IO4=15, type='Single', Min_Level=0, Max_Level=10, Min_duty=0,
                 Max_duty=1023):
        self.DOUBLEMOTOR = False
        self.DOUBLEMOTOR_DIRECTIONAL = False
        self.servo_IN1 = PWM( Pin( IO1 ), freq=50 )
        self.servo_IN2 = PWM( Pin( IO2 ), freq=50 )
        self.Min_Move_Level = Min_Level
        self.Max_Move_Level = Max_Level
        self.Min_DUTY = Min_duty
        self.Max_DUTY = Max_duty
        if 'Double' in type:
            if type == 'Double_directional':
                self.DOUBLEMOTOR = True
            else:
                self.DOUBLEMOTOR_DIRECTIONAL = True
            self.servo_IN3 = PWM( Pin( IO3 ), freq=50 )
            self.servo_IN4 = PWM( Pin( IO4 ), freq=50 )
            # self.motor = self.servo.duty( 500 )

    def forward(self, value):
        self.servo_IN1.duty( value )
        self.servo_IN2.duty( 0 )
        if self.DOUBLEMOTOR:
            self.servo_IN3.duty( value )
            self.servo_IN4.duty( 0 )

    def backward(self, value):
        self.servo_IN1.duty( 0 )
        self.servo_IN2.duty( value )
        if self.DOUBLEMOTOR:
            self.servo_IN3.duty( 0 )
            self.servo_IN4.duty( value )

    # OUT1,OUT2 to left motor, OUT3,OUT4 to right motor
    def turnleft(self, value):
        if self.DOUBLEMOTOR_DIRECTIONAL:
            self.servo_IN1.duty( 0 )
            self.servo_IN2.duty( value )
            self.servo_IN3.duty( value )
            self.servo_IN4.duty( 0 )

    def turnright(self, value):
        if self.DOUBLEMOTOR_DIRECTIONAL:
            self.servo_IN1.duty( value )
            self.servo_IN2.duty( 0 )
            self.servo_IN3.duty( 0 )
            self.servo_IN4.duty( value )

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
