# -*- coding: utf8 -*-
#!/usr/bin/env python

import socket
import sys
import binascii
import datetime
import time

def main():
<<<<<<< HEAD
    host = "172.16.1.61"
    port = 55555 #38317
=======
    host = "172.16.1.45"
    port = 9888#38317
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    
    id = 0
    while True:
<<<<<<< HEAD
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
=======
#        s.sendall(message.encode("utf8"))
        data = s.recv(512)
        if data:
            print(data.decode('utf8'))
#            print(data.hex())
            pass # null operation
        else:
            pass
#        message = input(" -> ")
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
#    s.send(b'--quit--')

if __name__ == "__main__":
    main()