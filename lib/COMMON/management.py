# class sort by name
class Sword_AP():
    ssid = 'Sword_AP'
    passwd = '123456789'
    IPprefix = '192.168.4.'
    class IO():
        MC_IN=22
        RELAY_OUT=27
    class CMD():
        Lhand='1:1-1'
        Rhand1='1_2:1-1'
        Rhand2='1_2:4-1' # S1,S2, begin from ON at once, next running is opposite of beginning, after interval of round = 4s, start by round-cycle, 1 round in all
        target='1:10-1'

class SWORD_Lhand(): # touch electrical light, it was foot before
    ssid = Sword_AP.ssid
    passwd = Sword_AP.passwd
    IPprefix = Sword_AP.IPprefix
    ID = 17
    S_Num = 1
    S1 = 4 #d2, GPIO4
    # cmd = '1:1-1' # S1, begin from ON immediately, next running is opposite of beginning, after interval of round= 0.5s,, start by round-cycle, 1 round in all.

class SWORD_Rhand(): # hold the swordWithMC
    ssid = Sword_AP.ssid
    passwd = Sword_AP.passwd
    IPprefix = Sword_AP.IPprefix
    ID = 18
    S_Num = 2
    S1 = 14 #d5, GPIO14
    S2 = 12 #d6, GPIO12
    # cmd_2 = '1_2:4-1' # S1,S2, begin from ON at once, next running is opposite of beginning, after interval of round = 4s, start by round-cycle, 1 round in all
    # cmd_2 = '1:8-5,2:2-9'  # S1,S2, begin from ON at once, next running is opposite of beginning, after interval of round = 4s, start by round-cycle, 1 round in all

class SWORD_target():
    ssid = Sword_AP.ssid
    passwd = Sword_AP.passwd
    IPprefix = Sword_AP.IPprefix
    ID = 19
    S_Num = 1
    S1 = 0  # d3, GPIO0
    # cmd = '1:10-1' # S1, begin from ON immediately, next running is opposite of beginning, after interval of round= 10s,, start by round-cycle, 1 round in all.

class CAR():
    ssid = 'CAR_AP'
    passwd = '123456789'
    IPprefix = '192.168.4.'
    ID = 13
    D_sensor = False

class Data_AP():
    ssid = 'Data_AP'
    passwd = '123456789'
    IPprefix = '192.168.4.'

class highSpeed():
    ssid = 'Data_AP'
    passwd = '123456789'
    ID = 2
    IPprefix = '192.168.4.'
    class branch1():
        ID = 3

class lowSpeed():
    ssid = 'Data_AP'
    passwd = '123456789'
    ID = 4
    IPprefix = '192.168.4.'

    class branch1():
        ID = 5

    class branch2():
        ID = 6


class powerStrip_AP():  # CAN'T BE HAVE BRANCH
    ssid = 'powerStrip_AP'
    passwd = '123456789'
    IPprefix = '192.168.4.'
    class CMD():
        No1 = '2:3-1'
        No2 = '2:3-1'

class powerStrip_1():
    ssid = powerStrip_AP.ssid
    passwd = powerStrip_AP.passwd
    IPprefix = powerStrip_AP.IPprefix
    ID = 8
    S_Num = 6
    S1 = 0  # GPIO 0
    S2 = 2
    S3 = 4
    S4 = 5
    S5 = 12
    S6 = 13


class powerStrip_2():
    ssid = powerStrip_AP.ssid
    passwd = powerStrip_AP.passwd
    IPprefix = powerStrip_AP.IPprefix
    ID = 9
    S_Num = 6
    S1 = 0  # GPIO 0
    S2 = 2
    S3 = 4
    S4 = 5
    S5 = 12
    S6 = 13

class MCBOX_IOassign(): # not using yet
    MC_IN=13
    VIBRATE=4
    MCPOWER=5

