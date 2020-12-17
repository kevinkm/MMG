from machine import Pin
from lib.COMMON.timer import Timer

class Force(): # using Timer
    def __init__(self, IO, funclist, funcP=None, diffi='normal'):
        # from lib.management import MCBOX_IOassign
        # self.IO={'MC':Pin( IO.MC_IN, Pin.IN ), 'VIBRATE':Pin( MCBOX_IOassign.VIBRATE, Pin.OUT ), 'MCPOWER':Pin( MCBOX_IOassign.MCPOWER, Pin.OUT )}
        self.IO={'MC' : Pin( IO.MC_IN, Pin.IN,Pin.PULL_DOWN )}
        # self.IO['MCPOWER'].value( 1 )
        # self.IO['VIBRATE'].value( 0 )
        self.MCtimes, self.round = 0, 0
        self.failedRound = 35
        self.funclist=funclist
        self.funcP=funcP
        self.target_i = len(funclist)
        self.RunAfter = Timer.RunAfter
        self.gotForce = 0

        if diffi == 'easy':
            self.MCthreshold = 3
        elif diffi == 'normal':
            self.MCthreshold = 5
        elif diffi == 'hard':
            self.MCthreshold = 9

    def reset_parameters(self):
        self.MCtimes = 0
        self.round = 0
        print ('a round, reset parameters ')

    @property
    def forceON(self):
        # self.conn.Main()
        if self.gotForce==0: # when inputDone=1, force_both stop working, but sword_srv start to work, details to see sword_main.py
            if self.RunAfter( 'countMC_1000' ):
                # if self.IO['MC'].value() == 1 or 1:  # for test
                if self.IO['MC'].value():  # run officially
                    self.MCtimes += 1
                self.round += 1
                if (self.round >= 10):
                    if self.MCtimes >= self.MCthreshold:
                        # self.runTrigger()
                        if self.MCthreshold == 3:  # 3 means easy
                            # run all ID once
                            for i in range(len(self.funclist)):
                                    self.funclist[i]( self.funcP )
                            print ('bodyID and targetID')
                        elif self.MCthreshold > 3: # greater than 3 means normal or hard
                            if self.target_i == 1:
                                print( 'Run Final func' )
                                self.funclist[0]( self.funcP )
                                self.target_i = len (self.funclist) # reset target_i
                                self.gotForce = 1 #when inputDone=1, MC stop working, but sword_srv start to work, details to see sword_main.py
                            elif self.target_i > 1:
                                self.funclist[self.target_i-1]( self.funcP )
                                print('The running func is no.: ', self.target_i )
                                self.target_i -= 1
                        else:
                            print ('fail to activate')
                    self.reset_parameters()
        else:
            return 1
