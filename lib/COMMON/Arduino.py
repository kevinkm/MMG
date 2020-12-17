class Arduino_func():
    __slots__ = ('leftMin', 'leftMax', 'rightMin','rightMax')
    def __init__(self, leftMin, leftMax, rightMin, rightMax ):
        self.leftMin = leftMin
        self.leftMax = leftMax
        self.rightMin = rightMin
        self.rightMax = rightMax

    def map(self, value, order=1):
        if value < self.leftMin or value > self.leftMax:
            return None
        # Figure out how 'wide' each range is
        leftSpan = self.leftMax - self.leftMin
        rightSpan = self.rightMax - self.rightMin
        # Convert the left range into a 0-1 range (float)
        valueScaled = float( value - self.leftMin ) / float( leftSpan )
        # Convert the 0-1 range into a value in the right range.
        if order == 1:
            return int( self.rightMin + (valueScaled * rightSpan) )
        elif order == -1:
            return int( (self.rightMin + self.rightMax) - (self.rightMin + (valueScaled * rightSpan)) )
'''
#Usage:
arduino_map=Arduino_map(0,180,30,120)
arduino_map(150)
#it will return a number between 30 to 120, which due to the value that scaled ascending order by 0 to 180,
#if "-1" as one of parameters
arduino_map.map(150,-1)
# it will be scaled descending order by 180 to 0
'''


