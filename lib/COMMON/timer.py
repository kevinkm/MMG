import time
class Timer():
    __slots__ = ['RunAfter', 'ticksAdd', 'ticks_ms_3', 'delayMS', 'ticks_ms', 'ticks_add', 'delay_ms']
    def delayMS(t):
        time.sleep( (t / 1000) )
    def ticks_ms_3():
        return int( time.time() * 1000 )
    def ticksAdd(a, b):
        return a + b
    def init():
        # global ticks_ms, ticks_add, delay_ms
        print ('\nInit timer')
        import sys
        if 'esp' in sys.platform:
            print( '\nESP SYSTEM\n' )
            Timer.ticks_ms = time.ticks_ms
            # Timer.ticks_add = time.ticks_add
            Timer.ticks_add = Timer.ticksAdd
            Timer.delay_ms = time.sleep_ms
        else:
            print( 'NOT ESP SYSTEM' )
            Timer.ticks_ms = Timer.ticks_ms_3
            Timer.ticks_add = Timer.ticksAdd
            Timer.delay_ms = Timer.delayMS
        del sys
    def RunAfter(str1):
        if str1 not in globals().keys():
            globals()[str1] = Timer.ticks_add( Timer.ticks_ms(), int( str1.split( '_' )[1] ) )
        elif globals()[str1] - Timer.ticks_ms() < 0:
            del (globals()[str1])
            return True
        else:
            return False
