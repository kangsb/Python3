# -*- coding: utf8 -*-
#!/usr/bin/env python

import socket
import sys
import binascii
import datetime
import time

def main():
    host = "172.16.1.61"
    port = 55555 #38317
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    
    id = 0
    while True:
        id += 1
        message = str(id)
        s.sendall(message.encode("utf8"))
        data = s.recv(5120)
        now = datetime.datetime.now()

        if data:
#            data = binascii.hexlify(data).decode()
#            data.hex()
            print(now, end =": ")
            print(data)
        else:
            print(now, end =": ")
            print("Socket closed")
            s.close()
            exit()
        
        time.sleep(1);
#    s.send(b'--quit--')

if __name__ == "__main__":
    main()