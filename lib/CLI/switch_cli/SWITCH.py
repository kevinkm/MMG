from lib.COMMON.timer import Timer

class Switch( object ): # using timer
    def __init__(self, conn):
        self.conn = conn
        self.CMDing = 0
        self.RunAfter = Timer.RunAfter
        # a = lambda x,y: int( x.split( '-' )[y])
        # self.setgpio = lambda b,bool: conn.slotToGPIO[a(b,0)].value( a(b,1) if bool == 1 else a(b,1) )
        # self.setgpio = lambda b,bool: conn.slotToGPIO[a(b,0)].value( bool )
        # self.setgpio = lambda b: conn.slotToGPIO[a(b,0)].value( a(b,1) )
        self.setgpio = lambda b,bool: conn.slotToGPIO[int(b)].value( bool )
    def setstatus(self,i):
        for j in self.slots[i]:  # Change the status of the list of Slots.
            self.setgpio(j, self.status[i])
            # print('SET STATUS IS ', self.status[i])

    def MSG(self, data):
        if self.CMDing:     # while in process of CMDing, can receive new data, but can't deal with it
            for i in range( len( self.slots ) ):
                if self.rounds[i]>0:
                    if self.RunAfter ( self.interval[i] ):
                        print('CHANGE status of switch')
                        # print ('running in CMDing')
                        self.status[i] = not self.status[i]
                        self.setstatus(i)
                        if self.status[i]==0: # when status is OFF, rounds - 1 ??
                            self.rounds[i] -= 1
                        if self.rounds[i] == 0:
                            self.setstatus(i)
                            self.countTimes -= 1
                            # print( '\ncountTimes -1 \n' )
                            if self.countTimes==0:
                                self.CMDing = 0
                                print( '\nDone! You can receive data\n' )
                        # print (self.rounds[i])
                        # print('\n\n\nswitch to', self.S,'\n\n\n')

        elif data!=None:
            self.slots, self.interval, self.rounds, self.status, b2, = [], [], [], [], []
            # print ('data:',data)
            a = data.split(',')
            for i in range(len(a)):
                aa = a[i].split(':')[0]
                if '_' in aa:
                    for j in aa.split('_'):
                        b2.append(j)
                        self.setgpio(j,True)
                    self.slots.append( b2 )
                    b2=[]
                else:
                    self.setgpio( aa, True ) # set GPIO high
                    # print ('set GPIO high')
                    self.slots.append( aa )
                self.interval.append('MSG'+str(i)+'_' + str(int(a[i].split(':')[1].split( '-' )[0]) * 1000))
                self.rounds.append(int(a[i].split(':')[1].split('-')[1]))
                self.status.append(True) # each of status of switch is ON
                self.countTimes = len( self.slots )
                self.CMDing = 1
                self.conn.switchMSG = None # useless?
            # print('slots:', self.slots, ' times:', self.rounds, ' interval:', self.interval, ' status:', self.status )

    def recvRepeatMSG_loop(self):
        if self.CMDing or self.conn.switch_loop() :
            # print ('LOOPing',self.conn.switchMSG,' self.runing',  self.running)
            self.MSG(self.conn.switchMSG)
