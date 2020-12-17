import socket
import time
import network
from lib.COMMON.timer import Timer

class microMSG_server():
    def __init__(self, WIFI, test=0):
        ap = network.WLAN(network.AP_IF)  # create access-point interface
        ap.active(1)  # activate the interface
        ap.config(essid=WIFI.ssid, password=WIFI.passwd,authmode=4,channel=9)  # set the ESSID of the access point
        time.sleep_ms(3000)
        self.printTest=test # only for test, control by main.py
        self.shake_port = 700
        # self.competition_port = 900
        self.regularData_port = 1000
        # self.competition_users_num = 0
        self.shake_socket = socket.socket()  # get instance
        self.shake_socket.bind(('0.0.0.0', self.shake_port))  # bind host address and port together
        self.shake_socket.listen(5)
        self.shake_socket.settimeout(0)
        self.N_socket = socket.socket()  # get instance
        self.N_socket.bind(('0.0.0.0', self.regularData_port))  # bind host address and port together
        self.N_socket.listen(5)
        self.N_socket.settimeout(0)
        self.data_len = 10
        self.Hdata_str = None
        self.Ldata_str = None
        self.shakeData_len = 6
        # self.compRecv_len = 1
        self.recv_List = []
        self.isHighSpeed = [0, 0, 0, 0, 0]
        self.H_conn = ['H_conn0', 'H_conn1', 'H_conn2', 'H_conn3', 'H_conn4']
        self.H_checkOnline = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        self.H_socket = {'H_socket0': 800, 'H_socket1': 801, 'H_socket2': 802, 'H_socket3': 803, 'H_socket4': 804}
        self.isGet_H = 0
        self.shakeToLData_dict = {} # i don't remember, but it may be only for competition.
        self.switch_dict = {}
        self.isSendSwitch = {}
        # Timer.init() # run in boot.py
        self.RunAfter = Timer.RunAfter

    def updateSwitch(self, ID, cmd):
        self.switch_dict['%04d' % ID] = [cmd, True]
        print ('%04d' % ID,'update switchDict: ',self.switch_dict['%04d' % ID])
        # print ('update switchDict: ',self.switch_dict)

    def try_connAccept(self, conn1):
        try:
            conn, addr = conn1.accept()
            return conn
        except:
            pass
        return 0

    def wait_newconn(self):
        if self.RunAfter('newConn_1100'):
            try:
                # print ('check newConn in every 1.1s')
                conn1, addr = self.shake_socket.accept()  # just use addr here, addr is ip, it's same like online_socket.
                conn1.settimeout(
                    2.8)  # timeout for 3s to receive the shakeData, do not use -1, incase signal just block for awhile
                # print ('checked newConn ')
                try:
                    shakeData = self._recv_data(conn1, self.shakeData_len)
                except:
                    print( 'no shakeData, it may a switch_cli' )
                    pass
                conn1.settimeout(0)
                conn1.close()
                print( 'GOT SHAKE_DATA: ' + shakeData )
                if shakeData[0] != '_':
                    # Add into list
                    self.shakeToLData_dict[shakeData] = ''
                    # USAGE: constantly use client, it needs to start after the previous one has been settled down.
                    if shakeData[-2:-1] == 'H':
                        i = int(shakeData[-1:])  # i is the number of channel
                        # print( 'HighSpeed' )
                        # STEP ONE, create socket in port( 8000) to receive length of H_data
                        socketLength = socket.socket()
                        # print( 111111111 )
                        socketLength.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        socketLength.bind(('0.0.0.0', 8000))
                        # print( 222222222 )
                        socketLength.listen(5)
                        socketLength.settimeout(10)
                        connLength = self.try_connAccept(socketLength)
                        if connLength != 0:
                            connLength.settimeout(5)  # keep 5s, very important before create high speed connection.
                            recv = self._recv_data(connLength, 4)
                            # print( 3333333333 )
                            print( 'recv from connLength: ' + recv )
                            # send length back
                            if recv != '_':
                                self.Hdata_len = int(recv)
                                # self.Hcheck=['*' for i in range( self.Hdata_len )] # no need.
                                print( 'receive length: ' + recv + ' NOW send OK back' )
                                self._send_data(connLength, 'OK')
                                print( 'CLOSE    connLength      AND     socketLength  ' )
                            else:
                                print( 'can not recv length H_ch' )
                                pass
                        else:
                            print( 'NO request port 8000, done.' )
                            pass

                        # STEP TWO, create socket in port(800...804) to receive H_data as such
                        if connLength != 0:
                            H_socket = list(sorted(self.H_socket.keys()))[i]  # get data from position 0
                            globals()[H_socket] = socket.socket()  # this line must after try.
                            globals()[H_socket].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            globals()[H_socket].bind(
                                ('0.0.0.0', self.H_socket[H_socket]))  # bind host address and port together
                            globals()[H_socket].listen(5)
                            globals()[H_socket].settimeout(5)
                            print( 'bound port: ' + str( self.H_socket[H_socket] ) )
                            globals()[self.H_conn[i]] = self.try_connAccept(globals()[H_socket])
                            print (globals()[self.H_conn[i]])
                            if globals()[self.H_conn[i]] != 0:
                                globals()[self.H_conn[i]].settimeout(0.05)
                                self.isGet_H = 1
                                self.isHighSpeed[i] = 1
                                print( 'start to receive high speed data ' )
                                connLength.close()
                                socketLength.close()
                            else:
                                print( 'NO connections-request on port ' + str( i ) )
                                pass
                    # self.competition_users_num += 1
            except:
                pass

    '''   
    def competition_server(self, Setnum_Users):
        # competition_conn = List_NormalCHANNEL_conn
        competition_conn = list(self.shakeToLData_dict.keys())

        def sendTOALLcompetition(str):
            for i in competition_conn:
                self._send_data(globals()[competition_conn[i]], str)

        def recvTOALLcompetition():
            for i in competition_conn:
                data = self._recv_data(globals()[competition_conn[i]], self.compRecv_len)
                if data[0] == '_':
                    self.competition_users_num -= 1
                    competition_conn.pop(i)

        def begin_competition():
            if self.RunAfter('competition_1000', 4):
                sendTOALLcompetition('B')

        if self.competition_users_num >= Setnum_Users:
            begin_competition()
            # confrontation loop start from here
            while 1:
                # begin at first time
                if self.competition_users_num > 1:
                    if self.RunAfter('competition_1000'):
                        recvTOALLcompetition()
                # Winner is born
                elif self.competition_users_num == 1:
                    globals()[competition_conn[0]].send(b"W")
                    self._recv_data(globals()[competition_conn[Setnum_Users]],
                                    self.compRecv_len)  # important clear buffer
                    return globals()[competition_conn[0]]
                # reset parameters for startover
                elif self.competition_users_num == 0:

                    begin_competition()
    '''

    def _send_data(self, conn, str):
        conn.send( str.encode() )

    def _recv_data(self, conn, length):
        self.connAccept = conn
        try:
            if length == self.shakeData_len or length == 4:
                recv = self.connAccept.recv(length).decode()
            else:
                self.connAccept = conn.accept()[0]
                recv = '_'
                while 1:
                    try:
                        recv = self.connAccept.recv(length).decode()
                        time.sleep(0.01)
                        # self.recv_List.append(recv)
                        shakeData = recv[:self.shakeData_len]
                        self.shakeToLData_dict[shakeData] = recv[self.shakeData_len:]
                        # globals()['online' + shakeData] = 1
                        break
                    except:
                        pass
        except:
            # List_CheckOnlineCHANNEL_conn.append( Var_Name_str )
            recv = '_'
        return recv

    def _get_L(self):
        recv = self._recv_data(self.N_socket, self.shakeData_len + self.data_len)  # recv has included accept()
        if recv != '_':
            shakedata = recv[:self.shakeData_len]
            uniqueid = shakedata[:4]
            rawdata = recv[self.shakeData_len:]
            if shakedata[-2:] == 'S_':  # 'receive a swicth request'
                print( 'receive a switch_cli request, id is: ', uniqueid )
                # problem:
                # 1. if isSendSwitch=Bool, it turns False since updateed, but  other switch may need to update
                # 2. if isSendSwitch is num, it will add up when
                # if self.isSendSwitch > 0 :
                try:
                    a=self.switch_dict[uniqueid][1]
                except:
                    print('No this ID ' + uniqueid + ' in switch_dict')
                    a=0
                if a :
                    self._send_data(self.connAccept, shakedata + self.switch_dict[uniqueid][0])
                    self.switch_dict[uniqueid][1] = False
                    print('\nsending updated data to client for switch_cli:',shakedata + self.switch_dict[uniqueid][0],'\n\n')
                elif rawdata == 'check':
                    self._send_data(self.connAccept, shakedata + 'check')
                    print( 'check client for switch_cli' )
                # else: # this is for test
                #     print( 'no need to response for switch_cli request! ' )
                #     pass
                self.connAccept.close()
            elif shakedata[-2:] == 'L_':
                self.Ldata_str = recv[self.shakeData_len:]
                if self.printTest == 1:
                    print( 'Ldata_str: ' + recv )
                self.connAccept.close()

    def _get_H(self, i, conn):
        try:
            recv = conn.recv(self.Hdata_len).decode()  # don't use _recv_data()
        except:
            recv = '_'

        if recv == '_':
            self.Hdata_str = None
            self.H_checkOnline[i] += 1
            # accumulation greater than 200
            if self.H_checkOnline[i] > 100:  # 100 = about 10s
                self.isHighSpeed[i] = 0
                self.H_checkOnline[i] = 0
                conn.close()  # close accept
                globals()[list(sorted(self.H_socket.keys()))[i]].close()  # close socket
                print( 'high speed CHANNEL-' + str( i ) + ' has got lost: ' )
                print( list( sorted( self.H_socket.keys() ) )[i] + ' closed' )
                del (globals()[self.H_conn[i]])
                print( self.H_conn[i] + ' closed' )
                del (globals()[list(sorted(self.H_socket.keys()))[i]])
                self.Hdata_str = 'offline'
        else:
            self.H_checkOnline[i] = 0
            self.Hdata_str = recv if '*' not in recv else None
            if self.printTest==1:
                print( 'Hdata_str: ' + self.Hdata_str )


    def start_server(self):
        if self.isGet_H and self.RunAfter('HS_50'):
            for i in range(5):
                if self.isHighSpeed[i]:
                    self._get_H(i, globals()[self.H_conn[i]])
        if self.RunAfter('lowSpeed_350'):
            self._get_L()


    def Main(self): # put it into "while" statement
        self.wait_newconn()
        self.start_server()
