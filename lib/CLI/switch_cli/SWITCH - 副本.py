from lib.COMMON.timer import Timer

class Switch( object ): # using timer
    def __init__(self, conn):
        self.conn = conn
        self.running=0
        self.RunAfter = Timer.RunAfter
        self.S = 1
        a = lambda x,y: int( x.split( '-' )[y])
        # self.setgpio = lambda b,bool: conn.slotToGPIO[a(b,0)].value( a(b,1) if bool == 1 else a(b,1) )
        self.setgpio = lambda b,bool: conn.slotToGPIO[a(b,0)].value( bool )

    def runMSG(self,data):
        if self.running:
            # print (self.b,self.times,self.interval)
            for i in range(len(self.b)):
                if self.times[i]>0:
                    # print (self.interval[i])
                    if self.RunAfter ( self.interval[i] ):
                        self.S = not self.S
                        print ('setgpio, self.b[i] and self.S ,:', self.b[i],self.S)
                        self.setgpio(self.b[i], self.S)
                        self.times[i] = self.times[i] - 1
                        # print('\n\n\nswitch to', self.S,'\n\n\n')
                else:
                    self.countTimes-=1
                    if self.countTimes==0:
                        self.running=0
                        # print ('\n\n\nrunning stopped\n\n')

        elif data!=None:
            self.b, self.interval, self.times = [], [], []
            # print ('data:',data)
            a = data.split(',')
            for i in range(len(a)):
                aa = a[i].split(':')[0]
                if '_' in aa:
                    self.b += [i + '-' + aa.split('-')[1] for i in aa.split('-')[0].split('_')]
                else:
                    self.b.append(aa)
                self.interval.append('MSG'+str(i)+'_' + str(int(a[i].split(':')[1].split( '-' )[0]) * 1000))
                self.times.append( int(a[i].split(':')[1].split('-')[1]) )
                self.countTimes=len(self.b)
                self.running=1
                self.conn.switchMSG = None
            self.setgpio(self.b[i], self.S)
            print ('setgpio, self.b[i] and self.S ,:', self.b[i],self.S)

    def recvRepeatMSG_loop(self):
        if self.conn.switch_loop() or self.running:
            # print ('LOOPing',self.conn.switchMSG,' self.runing',  self.running)
            self.runMSG(self.conn.switchMSG)

    #
    # def loop(self):
    #     if self.conn.switch_loop(): # This is for updating data
    #         if (self.conn.switchData)==('body'):  # msg isn't working now, ID control everything
    #             self.run_topic()
    #         elif (self.conn.switchData)==('target'):
    #             self.run_topic_target()
