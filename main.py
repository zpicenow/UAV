# -* -coding: UTF-8 -* -

import time, socket, threading
import serial
import serial.tools.list_ports
from queue import Queue
from datetime import datetime

port_list = list(serial.tools.list_ports.comports())
port_list_name = []


class SerialPort:
    def __init__(self,port,buand,queue):
        self.port = serial.Serial(port,buand)
        self.port.close()
        self.data = queue
        if not self.port.isOpen():
            self.port.open()
    def port_open(self):
        if not self.port.isOpen():
            self.port.open()
    def port_close(self):
        self.port.close()
    def send_data(self):
        while True:
            # date = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            val = self.data.get()

            # print("send:",val)

            self.port.write(val)

            print("send over")

            # time.sleep(1)
    def read_data(self):
        while True:
            count = self.port.inWaiting()
            if count > 0:
                rec_str = self.port.read((count))
                print("receive:",rec_str.decode())
def show_all_com():
    if len(port_list) <= 0:
        print("the serial port can't find")
    else:
        for items in port_list:
            port_list_name.append(items.device)

class UDPConnect:
    def send(self):
        while True:
            self.sock.sendto("hello".encode("utf-8"), ("sz.chenqs.cn", 1151))
            time.sleep(6)


def log(strLog):
    strs = time.strftime("%Y-%m-%d %H:%M:%S")
    print
    strs + "->" + strLog


class pipethread(threading.Thread):
    '''
   classdocs
    '''

    def __init__(self, source, sink):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        log("New Pipe create:%s->%s" % (self.source.getpeername(), self.sink.getpeername()))

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data: break
                self.sink.send(data)
            except Exception as ex:
                log("redirect error:" + str(ex))
                break
        self.source.close()
        self.sink.close()


class portmap(threading.Thread):
    def __init__(self, port, newhost, newport, local_ip=''):
        threading.Thread.__init__(self)
        self.newhost = newhost
        self.newport = newport
        self.port = port
        self.local_ip = local_ip
        self.sock = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.local_ip, port))
        self.sock.listen(5)
        log("start listen protocol:%s,port:%d " % ('tcp', port))

    def run(self):
        while True:
            fwd = None
            newsock = None
            newsock, address = self.sock.accept()
            log("new connection->protocol:%s,local port:%d,remote address:%s" % ('tcp', self.port, address[0]))
            fwd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                fwd.connect((self.newhost, self.newport))
            except Exception as ex:
                log("connet newhost error:" + str(ex))
                break
            p1 = pipethread(newsock, fwd, self.protocol)
            p1.start()
            p2 = pipethread(fwd, newsock, self.protocol)
            p2.start()


class pipethreadUDP(threading.Thread):
    def __init__(self, connection, connectionTable, table_lock):
        threading.Thread.__init__(self)
        self.connection = connection
        self.connectionTable = connectionTable
        self.table_lock = table_lock
        log('new thread for new connction')

    def run(self):
        # baunRate = 115200
        # print("1,list all com")
        # show_all_com()
        # print(port_list_name)
        # print("2,open write port",port_list_name[0])
        # serialPort_w = port_list_name[0]
        # mSerial_w = SerialPort(serialPort_w,baunRate)


        while True:
            try:
                '''
                data rewrite here
                '''

                data, addr = self.connection['socket'].recvfrom(4096)
                '''
                create thread

                '''
                print("3--,start write thread")
                # t1 = threading.Thread(target=mSerial_w.send_data(data))
                # t1.setDaemon(True)
                # t1.start()

                log('recv from addr"%s' % str(addr))
            except Exception as ex:
                print("33,start write thread")
                log("recvfrom error:" + str(ex))
                break
            try:
                print("333,start write thread")
                self.connection['lock'].acquire()
                self.connection['Serversocket'].sendto(data, self.connection['address'])
                # log('sendto address:%s' % str(self.connection['address']))
            except Exception as ex:
                log("sendto error:" + str(ex))
                break
            finally:
                print("3333333,start write thread")
                self.connection['lock'].release()
            self.connection['time'] = time.time()
            print("344444,start write thread")
        self.connection['socket'].close()
        print("355555555,start write thread")
        log("thread exit for: %s" % str(self.connection['address']))
        self.table_lock.acquire()
        self.connectionTable.pop(self.connection['address'])
        self.table_lock.release()
        log('Release udp connection for timeout:%s' % str(self.connection['address']))


class portmapUDP(threading.Thread):
    def __init__(self, port, newhost, newport,queue, local_ip='10.249.46.41'):
        threading.Thread.__init__(self)
        self.newhost = newhost
        self.newport = newport
        self.port = port
        self.local_ip = local_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip, port))
        self.sock.sendto("hello".encode("utf-8"),("sz.chenqs.cn",1151))
        self.connetcTable = {}
        self.port_lock = threading.Lock()
        self.table_lock = threading.Lock()
        self.timeout = 300
        self.data = queue
        # ScanUDP(self.connetcTable,self.table_lock).start()
        log('udp port redirect run->local_ip:%s,local_port:%d,remote_ip:%s,remote_port:%d' % (
        local_ip, port, newhost, newport))

    def run(self):
        while True:
            val, addr = self.sock.recvfrom(4096)
            # print("rec data")
            self.data.put(val)
        #     connection = None
        #     newsock = None
        #     self.table_lock.acquire()
        #     connection = self.connetcTable.get(addr)
        #     newconn = False
        #     if connection is None:
        #         connection = {}
        #         connection['address'] = addr
        #         newsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #         newsock.settimeout(self.timeout)
        #         connection['socket'] = newsock
        #         connection['lock'] = self.port_lock
        #         connection['Serversocket'] = self.sock
        #         connection['time'] = time.time()
        #         newconn = True
        #         log('new connection:%s' % str(addr))
        #     self.table_lock.release()
        #     try:
        #         connection['socket'].sendto(val, (self.newhost, self.newport))
        #         ''''''
        #
        #         print("udp is run")
        #         # t2 = threading.Thread(target=mSerial_r.read_data)
        #         # t2.setDaemon(True)
        #         # t2.start()
        #         ''''''
        #     except Exception as ex:
        #         log("sendto error:" + str(ex))
        #         # break
        #     if newconn:
        #         self.connetcTable[addr] = connection
        #         t1 = pipethreadUDP(connection, self.connetcTable, self.table_lock)
        #         t1.start()
        # log('main thread exit')
        # for key in self.connetcTable.keys():
        #     self.connetcTable[key]['socket'].close()


if __name__ == '__main__':
    queue = Queue()
    baunRate = 115200
    print("1,list all com")
    show_all_com()
    print(port_list_name)
    print("2,open write port", port_list_name[0])
    serialPort_w = port_list_name[0]
    mSerial_w = SerialPort(serialPort_w, baunRate,queue)
    # print("4.open read port ", port_list_name[1])
    # serialPort_r = port_list_name[1]
    # mSerial_r = SerialPort(serialPort_r, baunRate)
    myp = portmapUDP(60003, '10.249.46.41', 60004,queue)
    myp.start()
    print("3,start write thread")
    t1 = threading.Thread(target=mSerial_w.send_data)
    t1.setDaemon(True)
    t1.start()
    myp.join()
    t1.join()
    udpc = UDPConnect()
    udpTh = threading.Thread(target=udpc.send())
    udpTh.start()
    # myp.__stop()
