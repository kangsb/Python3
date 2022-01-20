
from datetime import datetime, timedelta
import time
import socket
import threading
import logging
import logging.handlers
import sys
import binascii

rcu_addr = '192.168.1.180'
#lmi_addr = '192.168.1.150'
lmi_addr = '192.168.1.174'
remote_port = 39009

to_rcu = (rcu_addr, remote_port)
to_lmi = (lmi_addr, remote_port)

class UdpSender(threading.Thread):
    def __init__(self, ssock, remoteaddr, port, log):
        threading.Thread.__init__(self)
        self.ssock = ssock
        self.remoteaddr = remoteaddr
        self.keyboardinterrupt = False
        self.log = log

    def run(self):
        self.log.info('Sender thread is now running...')
        self.ssock.sendto(b'7f', self.remoteaddr)
        index = 0
        while not self.keyboardinterrupt:
            time.sleep(1)
  
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
                if addr[0] == rcu_addr:
                    self.log.info('from RCU ' + msg.hex())
                    self.rsock.sendto(msg, to_lmi)
                elif addr[0] == lmi_addr:
                    #self.log.info('from LMI ' + msg.hex())
                    self.rsock.sendto(msg, to_rcu)
                lastesttime = curtime
            except socket.timeout:
                diff = curtime - lastesttime
                if diff > 5:
                    self.log.error("RX disconnected " + str(diff))
                    lastesttime = curtime

        self.log.info("Receiver thread terminated")

def main():
    global rcu_addr
    global lmi_addr
    global remote_port
    # for Logger
    fname = lmi_addr + "_" + str(remote_port) + ".log"
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
    remoteaddress = (lmi_addr, remote_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    #sock.setblocking(0)
    # Bind the socket to the port
    sock.bind(('', remoteaddress[1]))

#    myLogger.info('starting up on {} port {}'.format(*remoteaddress))
    txthread = UdpSender(sock, remoteaddress, remote_port, myLogger)
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
    