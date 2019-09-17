# -*- coding: utf8 -*-
#!/usr/bin/env python

import socket
import sys

def main():
    host = "172.16.1.45"
    port = 9888#38317
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()

    while True:
#        s.sendall(message.encode("utf8"))
        data = s.recv(512)
        if data:
            print(data.decode('utf8'))
#            print(data.hex())
            pass # null operation
        else:
            pass
#        message = input(" -> ")
#    s.send(b'--quit--')

if __name__ == "__main__":
    main()