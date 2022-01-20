
from datetime import datetime, timedelta
import time
import socket
import threading
import logging
import logging.handlers
import sys
import binascii
import struct

remote_addr = '172.16.1.41'
remote_port = 7272


class UdpEchoClient(threading.Thread):
    def __init__(self, rsock, log):
        threading.Thread.__init__(self)
        self.rsock = rsock
        self.keyboardinterrupt = False
        self.log = log

    def run(self):
        self.log.info('Udp echo client thread is now running...')
        lastesttime = time.time()
        id = 0
        while not self.keyboardinterrupt:
            curtime = time.time()
            try:
                id += 1
                self.rsock.sendto(str(id).encode('utf-8'), (remote_addr, remote_port))
                msg, addr = self.rsock.recvfrom(32)
                msg = msg.decode()
                self.log.info(msg)
                lastesttime = curtime
                if str(id) != msg:
                    self.log.error("Data mismatched: " + str(id) + " != " + msg)
            except socket.timeout:
                diff = curtime - lastesttime
                if diff > 2:
                    self.log.error("RX disconnected " + str(diff))
                    lastesttime = curtime
            except socket.error:
                pass
            #time.sleep(1)
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
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 10))
    #sock.setblocking(0)
    # Bind the socket to the port
    sock.bind(('', remoteaddress[1]))

    myLogger.info('starting up on {} port {}'.format(*remoteaddress))

    rxthread = UdpEchoClient(sock, myLogger)
    rxthread.start()

#    txthread.daemon = True
#    rxthread.daemon = True


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            myLogger.info("Sending kill to threads...")
            rxthread.keyboardinterrupt = True
            break

    rxthread.join()
    sock.close()

    myLogger.info("Program terminated")

if __name__ == '__main__':
    main()
    