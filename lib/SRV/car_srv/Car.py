from lib.COMMON.timer import Timer

class Car():
    def __init__(self, driver, steering, watchCar=None):
        if watchCar!=None:
            self.watchCar = watchCar
        else:
            self.watchCar = 0
        self.driver = driver
        self.servo = steering
        self.RunAfter = Timer.RunAfter
        self.engineData = {}
        self.lastM = 0
        self.stepDown = 0
        self.listStep = []
        self.lastM1 = ''
        self.lastData = ''
        self.sensitivity = 'ms_1000'
        self.D, self.M = '', ''
        self.forwardNO, self.backwardNO = 1, 1
        self.moveOn = 1
        self.A, self.last_D, self.current_D = 3, 0, 0
        self.T = 250
        self.delay = 't_400'

    def stepnum(self, num1, num2, M1):
        list1 = []
        j = num1 - num2
        if j > 0:
            for i in range( abs( j ) ):
                list1.append( M1 + str( num2 + i ) )
            list1.append( M1 + str( num1 ) )
        else:
            for i in range( abs( j ) ):
                list1.append( M1 + str( num1 + i ) )
            list1.append( M1 + str( num2 ) )
        return list1

    def stopcar(self, direction):
        if direction == 'F':
            self.forwardNO = 0
        elif direction == 'B':
            self.backwardNO = 0

    def engine(self, data, soloRemote):
        D, M = data
        self.engineData.update( {'direction': D, 'movement': M} if soloRemote else {
            'direction': data} if data[0] in ('L', 'R') else {'movement': data} )
        self.servo.turn( self.engineData['direction'] )
        if (self.forwardNO and self.engineData['movement'][0] == 'F') or (
                self.backwardNO and self.engineData['movement'][0] == 'B') or self.forwardNO == 0 and \
                self.engineData['movement'][
                    0] == 'B' or self.backwardNO == 0 and self.engineData['movement'][0] == 'F':
            self.driver.move( self.engineData['movement'] )
            self.forwardNO, self.backwardNO, self.moveOn = 1, 1, 1

    def go(self, data, soloRemote=1):
        if soloRemote == 0:
            pass
        else:
            if data == 'offline':
                self.driver.move( 'F00' )
                self.servo.turn( 'L00' )
            elif data != self.lastData and data != None:
                self.D, self.M = data.split( '-' )
                self.M, M1 = self.M[1:], self.M[:1]  # M1 is F or B
                if M1 != self.lastM1:
                    self.lastM = 0
                if int( self.M ) - (self.lastM) > 1:
                    self.listStep = self.stepnum( int( self.M ) - 1, self.lastM, M1 )
                    self.listStep.pop( 0 )  # already ranoll
                    self.M = '%02d' % (self.lastM + 1)
                    self.stepDown = 1
                    self.lastM = int( self.M )
                    self.M = M1 + self.M
                    self.engine( (self.D, self.M), soloRemote=soloRemote )
                else:
                    self.lastM = int( self.M )
                    self.M = M1 + self.M
                    self.stepDown = 0
                    # print( 'stepped The running is: ', self.D, M )
                    self.engine( (self.D, self.M), soloRemote=soloRemote )
                    try:
                        # del (globals()[delay])  # in order to run again in first
                        self.delay=...
                    except:
                        pass
                self.lastM1 = M1
                self.lastData = data
            elif self.stepDown:
                try:
                    if self.RunAfter( self.delay ):  # in order to slow down gryo action.
                        M1, self.M = self.listStep[0][:1], self.listStep[0][1:]
                        self.M = M1 + '%02d' % (int( self.M ) + 1)
                        self.listStep.pop( 0 )
                        self.engine( (self.D, self.M), soloRemote=soloRemote )
                except:
                    self.stepDown = 0

            if self.watchCar != 0:
                if self.RunAfter( self.sensitivity ):
                    self.sensitivity,self.moveOn = self.watchCar( self.stopcar, self.moveOn, self.driver,self.M)
