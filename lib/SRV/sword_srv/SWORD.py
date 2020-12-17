from machine import Pin
from lib.COMMON.timer import Timer
import time
from lib.COMMON.management import Sword_AP

class Sword(): # using Timer
    def __init__(self, IO, conn, func,force):
        self.conn=conn
        self.func=func
        self.force=force
        from lib.COMMON.management import SWORD_Lhand
        self.LhandID = SWORD_Lhand.ID
        del (SWORD_Lhand)
        from lib.COMMON.management import SWORD_Rhand
        self.RhandID = SWORD_Rhand.ID
        del (SWORD_Rhand)
        from lib.COMMON.management import SWORD_target
        self.targetID = SWORD_target.ID
        del (SWORD_target)
        self.IO = {'RELAY': Pin( IO.RELAY_OUT, Pin.OUT )}
        self.RunAfter = Timer.RunAfter
        self.L1,self.runTarget= 0, 0
        # self.FP,self.BP,self.LP,self.RP=0,0,0,0
        self.runON=1 # force will set it 1
        self.spinData,self.spinCount=20,0
        self.CTRLcar=0
        self.LaserON = 0
        self.F,self.B,self.L,self.R=0,0,0,0
        self.webrepl=0
        self.webreplON=1
        self.doneTARGET = 0
        self.TH1=1 # threshold 1, for activate the car

    def runWebrepl(self, v, w, x, y):
        # self.spinCount = 0  # reset spin gyro
        if self.webreplON:
            v += 1
            if v >40:
                self.runON = 0
                self.clickRelay( 1.2 )
                self.webrepl = 1
            elif (v > 0 and w == 0 and x == 0 and y == 0):
                print ('ready for webrepl :',v) # for test
                return v
            # run the next codes, you always have chance to switch webrepl, otherwise, Once a Chance!
            else:
                self.webreplON=0

    def clickRelay(self,t):
            self.IO['RELAY'].value(1)  # set relay ON, for 0.2
            time.sleep(t)
            self.IO['RELAY'].value(0)
            print ('clickRelay:',t )

    def activate_car(self, GYRO):
        data=int(GYRO[9:11])
        # if 1: # for test
        if self.TH1 and data < self.spinData: # officially
            self.spinCount += 1
            print ('spinCount',self.spinCount)
            # self.F, self.B, self.L, self.R = 0, 0, 0, 0    # no need to reset, because if spin, no chance to activate webrepl
        self.spinData = data
        if self.TH1 and self.spinCount>45:
            self.conn.updateSwitch( ID=self.LhandID, cmd=Sword_AP.CMD.Lhand )
            self.conn.updateSwitch( ID=self.RhandID, cmd=Sword_AP.CMD.Rhand2 )
            self.TH1 = 0
        elif self.TH1==0 and self.RunAfter('wait_3000'):
            print ('\nactivate_car\n')
            self.clickRelay(1.2)
            # self.TH1 = 1
            return 1
        else:
            return 0

    def activate_target(self, GYRO):
        TURN, GO = GYRO[0], GYRO[4]
        i, j = int( GYRO[1:3] ) , int( GYRO[5:7] )
        # if self.L3 or 1: # for test
        if self.runTarget : # officially
            if self.doneTARGET==0 and self.RunAfter( 'ii_3000' ):
                print ('run target')
                self.conn.updateSwitch( ID=self.targetID, cmd=Sword_AP.CMD.target ) # activate target
                # self.conn.updateSwitch(ID=self.LhandID, cmd=Sword_AP.CMD.Lhand)  # for test, because i need a hint
                print(self.conn.switch_dict, '\n')
                self.doneTARGET=1
            elif self.doneTARGET and self.RunAfter('ii_10000'):
                # self.conn.Main()  # To refresh conn.Ldata_str, make it not be 'Activate' , this is for the old code?? YES i think it's useless now, it's in "while" of main.py
                self.runTarget = 0
                self.clickRelay(1.2) # shutdown the sword.
                self.force.gotForce = 0 #MC can be input now
                self.doneTARGET = 0
                self.LaserON = 0
                self.runON=1
                self.spinCount=0
                # self.FP,self.BP,self.LP,self.RP=0,0,0,0
                print ('Target Mission has done, showdown the sword.')

        # elif self.FP and self.BP and self.LP and self.RP or 1:  # for test
        elif self.FP and self.BP and self.LP and self.RP:  # officially
            self.FP, self.BP, self.LP, self.RP = 0, 0, 0, 0
            self.conn.updateSwitch( ID=self.RhandID, cmd=Sword_AP.CMD.Rhand2 )  # the hand which hold the sword_srv, just activate 3s
            # self.conn.updateSwitch(ID=self.LhandID, cmd=Sword_AP.CMD.Lhand) # for test, because i need to see the both when im testing
            self.runTarget = 1

        # elif GO == 'F' and j > 7 or 1: # for test
        elif GO == 'F' and j > 7 : # officially
            self.F = self.runWebrepl(self.F, self.B, self.L, self.R) # keep gyro in the direction about 50*200ms
            if self.FP == 0:
                print('\nFP=1')
                self.func[0](self.conn)
                self.FP = 1
        # elif GO == 'B' and j > 7 or 1 : # for test
        elif GO == 'B' and j > 7: # officially
            self.B = self.runWebrepl(self.B, self.F, self.L, self.R)
            if self.BP == 0:
                print('\nBP=1')
                self.func[1](self.conn)
                self.BP = 1
        # elif l == 'L' and i > 7 or 1:# for test
        elif TURN == 'L' and i > 7:# officially
            self.L = self.runWebrepl(self.L, self.B, self.F, self.R)
            if self.LP == 0:
                print('\nLP=1')
                self.func[2](self.conn)
                self.LP = 1
        # elif l == 'R' and i > 7 or 1:# for test
        elif TURN == 'R' and i > 7:# officially
            self.R = self.runWebrepl(self.R, self.B, self.L, self.F)
            if self.RP == 0:
                print('\nRP=1')
                self.func[3](self.conn)
                self.RP = 1

    def run(self,GYRO):
        # if 1: # for test
        if self.runON: # for officially, why do i need runON, when go for webrepl, self.runON=0
            if GYRO==None: # when no install GYRO, test program
                GYRO='L00-F00-S00'
            if self.LaserON==0:
                self.clickRelay(0.2)
                # self.clickRelay(0.2, self-locked) # new plan, use globle var to make sure it run for once in time
                self.LaserON=1
                self.FP, self.BP, self.LP, self.RP = 0, 0, 0, 0
            if self.L1:
                if self.RunAfter('L1_200'):
                    self.activate_target(GYRO)
                    self.CTRLcar=self.activate_car(GYRO)

            elif self.L1==0: # the hand which touch electrical light,
                self.conn.updateSwitch( ID=self.LhandID, cmd=Sword_AP.CMD.Lhand ) # just activate 1s
                self.L1=1
                print('L1 activated')


