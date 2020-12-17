from machine import PWM,Pin
from lib.COMMON.Arduino import Arduino_func

class servo_MG996R():
    # d1-gpio5 for servo, d1-gpio5 as PWM
    __slots__ = 'IO', 'Level_min', 'Level_max','Straight','Left_max','Right_max'
    def __init__(self, IO=5, Level_min=0, Level_max=10, Straight=70, Left_max=50, Right_max=105):
        self.servo = PWM( Pin( IO ), freq=50 )
        self.servo.duty( Straight )
        # time.sleep( 1 )  # you may not need it
        self.Min_Turn_Level = Level_min
        self.Max_Turn_Level = Level_max
        self.Go_Straight = Straight
        self.Max_Turn_Left = Left_max
        self.Max_Turn_Right = Right_max

    def turn(self, value):
        duty_value = list( value )
        duty_value.pop( 0 )
        duty_value = int( ''.join( duty_value ) )
        if value[0] == 'L':
            arduino_map = Arduino_func( self.Min_Turn_Level, self.Max_Turn_Level, self.Max_Turn_Left,
                                             self.Go_Straight )
            duty_value = arduino_map.map( duty_value, -1 )
        elif value[0] == 'R':
            arduino_map = Arduino_func( self.Min_Turn_Level, self.Max_Turn_Level, self.Go_Straight,
                                             self.Max_Turn_Right )
            duty_value = arduino_map.map( duty_value )
        self.servo.duty( duty_value )
