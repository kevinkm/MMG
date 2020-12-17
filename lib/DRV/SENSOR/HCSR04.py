from machine import time_pulse_us,Pin
import time

class HCSR04:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, direction,trigger_gpio=15, echo_gpio=14, echo_timeout_us=500 * 2 * 30 ): #D8=IO15,D5=IO14
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin( trigger_gpio, mode=Pin.OUT, pull=None )
        self.trigger.value(0)
        self.direction=direction
        # Init echo pin (in)
        self.echo = Pin( echo_gpio, mode=Pin.IN, pull=None )
        self.sensor=1
        self._sensorRead=True
        self.A, self.last_D = 3, 0
        self.T = 250
        self.moveOn=...

    def _send_pulse_and_wait(self):
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    @property
    def vector(self):
        if self._sensorRead:
            pulse_time = self._send_pulse_and_wait()
            cms = (pulse_time / 2) / 29.1
            return self.direction +'-'+ (int(cms))

    def distance_cm(self):  # only for test
        pulse_time = self._send_pulse_and_wait()
        cms = (pulse_time / 2) / 29.1
        return cms

    def outputP(self, last, current, v):
        if last < current:
            return 30, 70, 100
        else:
            return 30 + v ** (self.A / 5), 70 + v ** (self.A / 5), 100 + v ** (self.A / 5)

    def outputTime(current, p, NowMove, SetMove):  # moveOn and stopcar and driver, need to be parameter
        if current < p[0]:
            return 100,True
        elif current > p[0]:
            return 250,False
        elif current > p[1]:
            return 350,False
        elif current > p[2]:
            return 1000,False

    def outputV(current, last, time):
        return abs( current - last ) / time * 1000

    def watchCar(self, stopcar, moveOn, driver, M):
        # program start
        if self._sensorRead == True:
            direction = self.vector.split( '-' )[0]
            current_D = ( self.vector.split( '-' )[1] )
            if current_D < 120:
                try:  # For the moment, start the car, distance <120, but no D, then occurs error.
                    self.T,STOP = self.outputTime( current=current_D,
                                              p=self.outputP( self.last_D, current_D,
                                                              v=self.outputV( current_D, self.last_D,
                                                                              self.T ) ) )
                    if STOP:
                        stopcar( direction[0] )
                        if moveOn and M[0] == direction[0]:
                            driver.move( 'F00' )
                            self.moveOn = False
                except:
                    print( 'try current_D < 120 got problem' )
                    pass
            else:
                self.T = 1000
            self.T = 100 if self.T == None else self.T
            sensitivity = 'ms_' + str( self.T )
            # figure out the distance
            self.last_D = current_D
        self._sensorRead = not self._sensorRead
        return self.moveOn, sensitivity
