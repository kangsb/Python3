
from datetime import datetime, timedelta
import time
import socket
import threading
import logging
import logging.handlers
import sys

remote_addr = '172.16.2.180'
remote_port = 39009
#172.16.2.53
class UdpSender(threading.Thread):
    def __init__(self, ssock, remoteaddr, log):
        threading.Thread.__init__(self)
        self.ssock = ssock
        self.remoteaddr = remoteaddr
        self.keyboardinterrupt = False
        self.log = log

    def run(self):
        self.log.info('Sender thread is now running...')
        index = 0
        while not self.keyboardinterrupt:
            darray = [['1A', '20', '48', '68', '81', 'A1', 'C1', 'E0'], ['0A', '21', '49', '69', '94', 'A0', 'C0', 'E0']]
            for var in darray[index]:
                data = bytes.fromhex(var)
                self.ssock.sendto(data, self.remoteaddr)
                time.sleep(0.1)
            if index == 0:
                index = 1
            else:
                index = 0
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
        logging.info('Receiver thread is now running...')
        lastesttime = time.time()
        while not self.keyboardinterrupt:
            curtime = time.time()
            msg, addr = self.rsock.recvfrom(512)
            self.log.info(msg.hex())
            diff = curtime - lastesttime
            if diff > 3:
                self.log.error("RX disconnected")
            lastesttime = curtime

        logging.info("Receiver thread terminated")

def main():
    # for Logger
    myLogFormatter = logging.Formatter('[%(asctime)s | %(levelname)s] %(message)s')

    #handler settings
    myLogHandler = logging.handlers.TimedRotatingFileHandler(filename='debug.log', when='midnight', interval=1, encoding='utf-8')
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
    remoteaddress = (remote_addr, remote_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setblocking(0)
    # Bind the socket to the port
    sock.bind(('', remoteaddress[1]))

    myLogger.info('starting up on {} port {}'.format(*remoteaddress))

    txthread = UdpSender(sock, remoteaddress, myLogger)
    rxthread = UdpReceiver(sock, myLogger)

#    txthread.daemon = True
#    rxthread.daemon = True

    txthread.start()
    rxthread.start()

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
    