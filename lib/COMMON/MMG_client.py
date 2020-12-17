'''
This is microMG, MG = message, go!
'''

import socket
import network
from machine import reset as machinereset
from lib.COMMON.timer import Timer

sta = network.WLAN( network.STA_IF )
sta.active( 1 )

class microMSG_client():
    # __slots__ = ['ID', 'switchlen', 'shakeData_port', 'H_port', 'regularData_port', 'H_failCount', 'LData_len','HdataLen_str','Hcheck','shakeData_len','switchOffCount','isHighSpeed','switchConn','']
    def __init__(self, apparatus,
                 h_CH='', Hdatalen=10, Ldatalen=10, Ltime=1000, isSendRepeat=1, switchMode=0): #h_CH=1...5
        # program start
        self.ID = 'ID' + '%04d' % apparatus.ID
        if Hdatalen == 'car':
            Hdatalen = 7
        if switchMode==1:
            from machine import Pin
            import time
            self.ran_switch = time.ticks_us() % 1000
            self.slotToGPIO={}
            for i in range( 1, apparatus.S_Num + 1 ):
                self.slotToGPIO.update( {i: Pin( apparatus.__dict__.get( 'S' + str( i ) ), Pin.OUT )} )
        self.switchlen = 31
        self.shakeData_port = 700
        self.H_port = [800, 801, 802, 803, 804]
        # self.competition_port = 900
        self.regularData_port = 1000
        self.H_failCount = 0
        self.LData_len = Ldatalen
        self.HdataLen_str = '%04d' % Hdatalen
        self.Hcheck = ''.join( ['*' for i in range( Hdatalen )] )
        self.shakeData_len = 6
        self.switchOffCount = 0
        self.isHighSpeed = 1
        # self.tempcount = 1
        self.switchConn = None
        import time
        self.ran_CL = (time.ticks_us() % 100) * 2
        # del (time)
        self.CLtime_ms = Ltime if Ltime >= 1000 else 1000
        self.isHalfduplex_recv = 1
        self.Latest_Hdata=None
        # self.switchData,self.switchStatus= '','ON'
        # Timer.init()
        self.RunAfter = Timer.RunAfter
        self.isSendRepeat=isSendRepeat
        # connect to WIFI , then socket
        if sta.isconnected() == 0:
            sta.ifconfig( (apparatus.IPprefix + str( apparatus.ID ), '255.255.255.0', apparatus.IPprefix + '1', apparatus.IPprefix + '1') )
            self.connectwifi( sta, apparatus.ssid, apparatus.passwd )
        else:
            print( 'WIFI has already CONNECTED' )

        # CREATE SHAKEDATA
        if h_CH != '':
            self.highSpeed_port = self.H_port[h_CH]
            self.shakeData = '%04d' % apparatus.ID + 'H' + str( h_CH )
        elif switchMode == 1:
            print( 'switch_cli MODE' )
            globals()['i' + '%04d' % apparatus.ID + 'runtimes'] = 0
            self.shakeData = '%04d' % apparatus.ID + 'S_'
            self.isSwitch = 1
        else:
            self.shakeData = '%04d' % apparatus.ID + 'L_'


        # IF HIGH SPEED
        if h_CH != '':
            # SEND SHAKE DATA
            self.sendUDP( port=self.shakeData_port, data=self.shakeData )
            print( 'sent self.shakeData : ' + self.shakeData )

            # SEND THE LENGTH OF HIGHSPEED, WAIT UNTIL RECEIVE STR: 'OK'
            conn, recvData = self.verifyTCP( self.HdataLen_str, 8000 )
            if recvData == 'OK':
                print( 'trying connect to high speed port: ' + str( self.highSpeed_port ) )
                self.H_clientSocket = self.try_connConnnect( int( self.highSpeed_port ) )
                if self.H_clientSocket != 1:
                    self.isHighSpeed = 1
                    self.H_clientSocket.settimeout( 0.1 )
                else:
                    print( '\n\nH_clientSocket is 1\n\n' )
                conn.close()
            else:
                print( ' can not receive the response from high speed port 8000 ' )
                Timer.delayMS(5000)

    def connectwifi(self, station, ssid, password):
        counter = 0
        station.disconnect()
        while station.isconnected() == 0:
            Timer.delayMS(1000)
            print(' is trying to connect WIFI')
            station.connect(ssid, password)
            Timer.delayMS(5000)
            counter += 1
            if counter >= 8 or station.isconnected() == 0:
                print('can not find the AP , go to sleep now!')

    def sendUDP(self, port, data):
        count = 0
        while 1:
            try:
                conn = socket.socket()
                conn.connect( ('192.168.4.1', port) )
                self._send_data( conn, data )
                conn.close()
                break
            except:
                count += 1
                Timer.delayMS(800)
                print( 'shake data can not send.' )
                if count > 4:
                    # uos.dupterm(uart, 1)  # for moment when test
                    machinereset()  # for moment when officially start to use


    def DoneSwitchconn(self):
        try:
            self.switchConn.close()
            self.switchConn=None
            print ('switchConn close succeed')
        except:
            print ('switchConn close failed')
            pass
        self.switchOffCount=0
        self.isHalfduplex_recv=1


    def verifyTCP(self, data, port, mode=''): # halfduplex means: send data in this round, receive data in next round
        if self.isHalfduplex_recv == 1: # "isHalfduplex_recv"  only for SWITCH MODE
            conn = self.try_connConnnect( int( port ) )
            if conn != 1:
                self._send_data( conn, data )
            else:
                print ('get conn of verifyTCP failed')
                self.DoneSwitchconn()
                return 1, 1
        else:
            conn = self.switchConn
        if conn != 1:
            if mode == '':
                conn.settimeout( 5 )
            elif mode == 'halfduplex' and self.isHalfduplex_recv == 1:
                conn.settimeout( 0 )
                self.isHalfduplex_recv = not self.isHalfduplex_recv
                return conn, 'responding'
            elif mode == 'halfduplex':
                self.isHalfduplex_recv = not self.isHalfduplex_recv

            recv = self._recv_data( conn, self.shakeData_len  + self.switchlen )  # receive: NO, OFF, OK, CHECK,
            return conn, recv


    def try_connConnnect(self, port):
        count = 0
        while count < 5:
            try:
                conn1 = socket.socket()
                conn1.connect( ('192.168.4.1', port) )
                return conn1
            except:
                count += 1
            Timer.delayMS(750)
        print( 'can not connect to server port: ' + str( port ) )
        return 1

    def _recv_data(self, conn, length):
        try:
            recv = conn.recv( length ).decode()

            if recv == '':# for test, able to be deleted.
                print( 'receive empty, try again' ) # for test, able to be deleted.
        except:
            recv = '_'
            print ('NO data can be received, so it will be _')
        return recv

    def _send_data(self, conn, str):
        conn.send( str.encode() )


    def switch_loop(self):
        recvData=''
        if self.isSwitch == 1:
            if self.RunAfter( self.ID + '_' + str( 1000 + self.ran_switch ) ):
                while recvData=='':
                    if self.RunAfter('tryRecv_150'):
                        if self.switchOffCount > 7: # if can't recv data over 7times, send 'check' to server to prove not offline.
                            self.switchConn, recvData = self.verifyTCP( self.shakeData + 'check', self.regularData_port,
                                                                        mode='halfduplex' )
                        else:
                            self.switchConn, recvData = self.verifyTCP( self.shakeData ,
                                                                        self.regularData_port, mode='halfduplex' )
                            print( 'Non-Responsed-Times is : ' + str( self.switchOffCount ) )
                if recvData not in ('responding', '_', 1):
                    self.switchConn.close()
                    rawdata = recvData[self.shakeData_len:]  # rawdata in switch_cli is 0 or 1
                    print ('\nGET SWITCH DATA: ', rawdata,'\n')
                    unique_ID = recvData[:4]
                    if unique_ID == self.ID[2:]:
                        self.switchOffCount = 0
                        if rawdata == 'check':
                            self.switchOffCount = 0
                        elif  ':' in rawdata:
                            self.switchMSG = rawdata
                            return 1  # funclib needs this
                        else: # when data you receive isn't : ON, OFF , check
                            b = rawdata.split( ',' )
                            for i in range( len( b ) ):
                                self.slotToGPIO[int( b[i].split( '-' )[0] )].value( int( b[i].split( '-' )[1] ) )
                else:
                    self.switchOffCount += 1
                    if self.switchOffCount > 24:
                        print ('recvData: ',recvData)
                        print( ' set switch_cli be offline' )

    def _send_L(self, data):
        if self.RunAfter( self.ID + '_' + str( self.CLtime_ms + self.ran_CL ) ):
            self.sendUDP( data=self.shakeData + data, port=self.regularData_port )
            print ('send L')

    def _send_H(self, data):
        if self.isHighSpeed and self.RunAfter( self.ID + '_50' ):
            try:
                if self.isSendRepeat or data != self.Latest_Hdata:
                    self.Latest_Hdata = data
                    self.H_clientSocket.send( self.Latest_Hdata.encode() )
                    self.H_failCount = 0
                elif self.RunAfter( self.ID + 'HC_14000' ):
                    self.H_clientSocket.send( self.Hcheck )
            except:
                Timer.delayMS(700)
                self.H_failCount += 1
                print( ' Highspeed data can not send.' )
                if self.H_failCount > 8:
                    self.isHighSpeed=1
                    print ('isHighSpeed 1')
                    return 1  # for moment when test
                    # machine.reset()  # for moment when officially start to use

    def Main(self):
        self.switch_loop()

    '''
    def competition_client(self, checkin):
        self.client_socket.settimeout( -1 )
        data = self._recv_data( self.client_socket, self.online_len )
        while data == 'B':
            # not yet, count down, and make a beep for 5s
            print( 'warning, MC check start after 5s' )
            Timer.delayMS(5000)
            while 1:
                Timer.delayMS( 1000 )  # save energy than run_after
                if checkin:
                    self._send_data( self.client_socket, '1' )
                    self.client_socket.settimeout( 0.2 )
                    if self._recv_data( self.client_socket, self.online_len ) == 'W':
                        print( 'winner' )
                        self.client_socket.settimeout( 0 )
                        data = '_'  # jump out the whole loop.
                else:
                    print( 'you out, waiting for next chance' )
                    self.client_socket.settimeout( -1 )
                    if self._recv_data( self.client_socket, self.online_len ) == 'B':
                        break
    '''
