
from datetime import datetime, timedelta
import time
import socket
import threading
import logging
import logging.handlers
import sys
import binascii
<<<<<<< HEAD
import struct

remote_addr = '172.16.1.60'
remote_port = 55555
=======

remote_addr = '172.16.1.180'
remote_port = 39004
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3

class UdpSender(threading.Thread):
    def __init__(self, ssock, remoteaddr, port, log):
        threading.Thread.__init__(self)
        self.ssock = ssock
        self.remoteaddr = remoteaddr
        self.keyboardinterrupt = False
        self.log = log

    def run(self):
        self.log.info('Sender thread is now running...')
        index = 0
<<<<<<< HEAD
        darray = [['21', '31', '41', '51', '61', '71', '81', '91'], ['21', '31', '41', '51', '61', '71', '81', '91']]
        while not self.keyboardinterrupt:
=======
        while not self.keyboardinterrupt:
#            darray = [['18', '20', '4E', '6E', '80', 'A0', 'C6', 'E1', 'F8'], ['18', '20', '4F', '6E', '80', 'A0', 'C6', 'E1', 'F8']]
            darray = [['18', '20', '4E', '6E', '80', 'A0', 'C6', 'E7', 'F8'], ['18', '20', '4F', '6E', '80', 'A0', 'C6', 'E7', 'F8']]
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
            for var in darray[index]:
                data = bytes.fromhex(var)
                self.ssock.sendto(data, self.remoteaddr)
#                self.log.info(binascii.hexlify(data))
            if index == 0:
                index = 1
            else:
                index = 0
<<<<<<< HEAD
            time.sleep(0.01) 
=======
            time.sleep(0.1)
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
  
        self.log.info("Sender thread terminated")
"""
            darray = '1220406080A0C0E0'
            data = bytes.fromhex(darray)
            self.ssock.sendto(data, self.remoteaddr)
"""

class UdpReceiver(threading.Thread):
    def __init__(self, rsock, log):
        threading.Thread.__init__(self)
        self.rsock = rsock
        self.keyboardinterrupt = False
        self.log = log

    def run(self):
        self.log.info('Receiver thread is now running...')
        lastesttime = time.time()
        while not self.keyboardinterrupt:
            curtime = time.time()
            try:
<<<<<<< HEAD
                msg, addr = self.rsock.recvfrom(32)
                #self.log.info(msg.hex())
                lastesttime = curtime
            except socket.timeout:
                diff = curtime - lastesttime
                if diff > 2:
                    self.log.error("RX disconnected " + str(diff))
                    lastesttime = curtime
            except socket.error:
                pass
            time.sleep(0.1)
=======
                msg, addr = self.rsock.recvfrom(512)
#                self.log.info(msg.hex())
                lastesttime = curtime
            except socket.timeout:
                diff = curtime - lastesttime
                if diff > 3:
                    self.log.error("RX disconnected " + str(diff))
                    lastesttime = curtime
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
        self.log.info("Receiver thread terminated")

def main():
    global remote_port
    global remote_addr
    if len(sys.argv) == 3:
        raddr = sys.argv[1]
        port = int(sys.argv[2])
    else:
        port = remote_port
        raddr = remote_addr
    
    remote_port = port
    remote_addr = raddr

    # for Logger
    fname = raddr + "_" + str(port) + ".log"
    myLogFormatter = logging.Formatter('[%(asctime)s | %(levelname)s] %(message)s')

    #handler settings
    myLogHandler = logging.handlers.TimedRotatingFileHandler(filename=fname, when='midnight', interval=1, encoding='utf-8')
    myLogHandler.setFormatter(myLogFormatter)
    myLogHandler.suffix = "%Y%m%d"

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(myLogFormatter)

    #logger set
    myLogger = logging.getLogger()
    myLogger.setLevel(logging.DEBUG)
    myLogger.addHandler(myLogHandler)
    myLogger.addHandler(streamHandler)

    # Create a UDP socket
    remoteaddress = (raddr, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
<<<<<<< HEAD
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 10))
=======
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
    #sock.setblocking(0)
    # Bind the socket to the port
    sock.bind(('', remoteaddress[1]))

    myLogger.info('starting up on {} port {}'.format(*remoteaddress))

    txthread = UdpSender(sock, remoteaddress, port, myLogger)
    txthread.start()
    rxthread = UdpReceiver(sock, myLogger)
    rxthread.start()

#    txthread.daemon = True
#    rxthread.daemon = True


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            myLogger.info("Sending kill to threads...")
            txthread.keyboardinterrupt = True
            rxthread.keyboardinterrupt = True
            break

    txthread.join()
    rxthread.join()
    sock.close()

    myLogger.info("Program terminated")

if __name__ == '__main__':
    main()
    