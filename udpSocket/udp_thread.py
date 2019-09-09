
from datetime import datetime, timedelta
import time
import socket
import threading
import logging
import logging.handlers
import sys
import binascii

remote_addr = '172.16.1.209'
remote_port = 39005

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
        while not self.keyboardinterrupt:
            darray = [['D1', '77']]#, ['08', 'AE'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F'], ['80', 'A0'], ['C6', 'E6'], ['F8', '1A'], ['20', '4F']]
            for var in darray[index]:
                data = bytes.fromhex(var)
                self.ssock.sendto(data, self.remoteaddr)
                self.log.info(binascii.hexlify(data))
            index += 1
            if index == 1:
                index = 0
            time.sleep(5)
  
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
                msg, addr = self.rsock.recvfrom(512)
#                self.log.info(msg.hex())
                lastesttime = curtime
            except socket.timeout:
                diff = curtime - lastesttime
                if diff > 5:
                    self.log.error("RX disconnected " + str(diff))
                    lastesttime = curtime

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
    