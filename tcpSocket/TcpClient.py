# -*- coding: utf8 -*-
#!/usr/bin/env python

import socket
import sys

def main():
    host = "172.16.1.51"
    port = 38317
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()

    while True:
#        s.sendall(message.encode("utf8"))
        if s.recv(5120).decode("hex") == "-":
            pass # null operation
        message = input(" -> ")
#    s.send(b'--quit--')

if __name__ == "__main__":
    main()