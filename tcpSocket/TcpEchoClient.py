# -*- coding: utf8 -*-
#!/usr/bin/env python

import socket
import sys
import binascii
import datetime
import time
from datetime import datetime, timedelta
import logging
import logging.handlers


def main():

    host = "172.16.1.41"
    port = 7171 #38317

    # for Logger
    fname = host + "_" + str(port) + ".log"
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

    myLogger.info("TCP echo client start")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    
    lastesttime = time.time()
    curtime = time.time()
    id = 0

    while True:
        id += 1
        message = str(id)

        try:
            s.sendall(message.encode('utf-8'))
            data = s.recv(5120)
            
            if data:
                data = data.decode('utf-8')
                curtime = time.time()
                myLogger.info(data)
                diff = curtime - lastesttime
                if data != message:
                    myLogger.error("Data mismatched: " + str(id) + " != " + data)
                if diff > 2:
                    myLogger.error("Delay: " + str(diff) + "sec")
                lastesttime = curtime
            else:
                myLogger.info("Socket closed")
                s.close()
                
        except socket.timeout:
            diff = curtime - lastesttime
            if diff > 2:
                myLogger.error("*Delay: " + str(diff) + "sec")
                lastesttime = curtime
        except socket.error:
            pass

        try:
            #time.sleep(1)
            pass
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            s.close()
            myLogger.info("Program terminated");
            break

if __name__ == "__main__":
    main()