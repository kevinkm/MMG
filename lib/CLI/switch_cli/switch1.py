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

    def runMSG(self,data):
        if self.CMDing:
            for i in range( len( self.slots ) ):
                # print( 'only i', i )
                if self.rounds[i]>0:
                    if self.RunAfter ( self.interval[i] ):
                        self.status[i] = not self.status[i]
                        if self.status[i] :
                            self.rounds[i] -= 1
                        print ('only i',i)
                        self.setstatus(i)
                        if self.rounds[i] == 0:
                            self.setstatus(i)
                            self.countTimes -= 1
                            print( '\ncountTimes -1 \n' )
                            if self.countTimes==0:
                                self.CMDing = 0
                                print( '\n\nDone! You can receive data\n\n' )
                        print (self.rounds[i])
                        # print('\n\n\nswitch to', self.S,'\n\n\n')
                # else:
                #     self.countTimes-=1
                #     print ('\ncountTimes -1 \n')
                #     if self.countTimes==0:
                #         self.CMDing=0
                #         print ('\n\nDone! You can receive data\n\n')

        elif data!=None:
            self.slots, self.interval, self.rounds, self.status, b2, = [], [], [], [], []
            # print ('data:',data)
            a = data.split(',')
            for i in range(len(a)):
                aa = a[i].split(':')[0]
                if '_' in aa:
                    # print ([i + '-' + aa.split('-')[1] for i in aa.split('-')[0].split('_')])
                    # self.b += [i + '-' + aa.split('-')[1] for i in aa.split('-')[0].split('_')]
                    # self.b.append([i + '-' + aa.split('-')[1] for i in aa.split('-')[0].split('_')])
                    # self.b.append([i for i in aa.split('_')])
                    for j in aa.split('_'):
                        b2.append(j)
                        self.setgpio(j,True)
                        print ('turn on:', j)
                    self.slots.append( b2 )
                    b2=[]
                else:
                    self.setgpio( aa, True )
                    print( 'turn on:', i )
                    self.slots.append( aa )
                self.interval.append('MSG'+str(i)+'_' + str(int(a[i].split(':')[1].split( '-' )[0]) * 1000))
                self.rounds.append(int(a[i].split(':')[1].split('-')[1]))
                self.status.append(True)
                self.countTimes = len( self.slots )
                self.CMDing = 1
                self.conn.switchMSG = None
            print('slots:', self.slots, ' times:', self.rounds, ' interval:', self.interval, ' status:', self.status )

            # for i in range(len(self.b)):
            #     self.setgpio(self.b[i])
            #     howto activate 1,2,1,3 maybe from line 41, is easier

            # print ('setgpio, self.b and self.S :', self.b,self.S)
            # [['1', '2'], ['1', '3']]

    def recvRepeatMSG_loop(self):
        if self.conn.switch_loop() or self.CMDing:
            # print ('LOOPing',self.conn.switchMSG,' self.runing',  self.running)
            self.runMSG(self.conn.switchMSG)

    #
    # def loop(self):
    #     if self.conn.switch_loop(): # This is for updating data
    #         if (self.conn.switchData)==('body'):  # msg isn't working now, ID control everything
    #             self.run_topic()
    #         elif (self.conn.switchData)==('target'):
    #             self.run_topic_target()
