# -*- coding:utf-8 -*-

import sys
import serial
import threading
from datetime import datetime, timedelta
import logging
import logging.handlers

class SerialComm:
    def __init__(self, port, baudrate, log):
        self.port = port
        self.baudrate = baudrate
        self.databit = 8
        self.stopbit = 1
        self.parity = serial.PARITY_EVEN # serial.PARITY_NONE
        self.flowcontrol = False
        self.alive = False
        self.receiver_thread = None
        self.sender_thread = None
        self.reader_alive = None
        self.ser_handler = None
        self.bLeasedLine = True
        self.log = log

    def open(self):
        self.ser_handler = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity)
#        self.modem_init()
        self._start_receiver()
        #self._start_sender()

    def _start_sender(self):
        """sender thread"""
        self.log.info('Sender thread now running')
        self.sender_thread = threading.Thread(target=self.sender, name='tx')
        self.sender_thread.daemon = True
        self.sender_thread.start()

    def _start_receiver(self):
        """receiver thread"""
        self.log.info('Receiver thread now running')
        self.reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_receiver(self):
        self.reader_alive = False
        self.receiver_thread.join()

    def reader(self):
        """loop and copy serial->console"""
<<<<<<< HEAD
        normal = ['1a', '20', '4f', '4e', '6e', '80', 'a0', 'c6', 'e6', 'f8' ]
=======
#        normal = ['1a', '20', '4f', '4e', '6e', '80', 'be', 'c6', 'e6', 'f8' ]
        normal = ['1a', '20', '48', '68', '95', 'be', 'c6', 'e6', 'f8' ]
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
        try:
            str_data = ''
            while self.ser_handler.is_open:
                # read all that is there or wait for one byte
                data = self.ser_handler.read(1) #(self.ser_handler.in_waiting or 1)
                if data:
                    hex_string = data.hex() #binascii.hexlify(data).decode('utf-8')
<<<<<<< HEAD
                    self.log.info(hex_string)
                    """    
                    if hex_string in normal:
                        self.log.info(hex_string)
                        pass
                    else:
                        self.log.error(hex_string)
                    """
=======
                    if hex_string in normal:
#                        self.log.info(hex_string)
                        pass
                    else:
                        self.log.error(hex_string)
>>>>>>> 71312fed43d3240538cc7e4b5045381cbd4c37c3
        except serial.SerialException as err:
            print(err.to_string())
            self.alive = False
            raise  # XXX handle instead of re-raise?

    def sender(self):
        while self.ser_handler.is_open:
            print("send hello")
            self.ser_handler.write(b'Hello')

    def modem_init(self):
        self.ser_handler.write(b'+++ATH\r\n')
        self.ser_handler.write(b'ATZ\r\n')
        # Reset modem to its factory defaults
        self.ser_handler.write(b'AT&F0\r\n')
        # Enables result codes.
        self.ser_handler.write(b'ATQ0\r\n')
        # echo off
        self.ser_handler.write(b'ATE1\r\n')
        # CONNECT result code reports DCE receive speed; enables protocol result codes.
        self.ser_handler.write(b'ATW2\r\n')
        if self.bLeasedLine:
            print('--- Leased line configuration, ')
            if self.flowcontrol:
                self.ser_handler.write(b'AT&L2&C1&D2&K3\r\n')
                print('use flowcontrol\n')
            else:
                self.ser_handler.write(b'AT&L2&C1&D2&K0\r\n')
                print('no flowcontrol\n')
        else:
            print('+++ Dial-up configuration, ')
            if self.flowcontrol:
                self.ser_handler.write(b'AT&L0&C1&D2&K3\r\n')
                print('use flowcontrol\n')
            else:
                self.ser_handler.write(b'AT&L0&C1&D2&K0\r\n')
                print('no flowcontrol\n')

        # S36 + S48, LAMP, MNP, or Async
        self.ser_handler.write(b'ATS36=7\r\n')
        self.ser_handler.write(b'ATS48=7\r\n')
        # S0, auto answer
        self.ser_handler.write(b'ATS0=1\r\n')
        # V.42 or MNP error control mode.
        self.ser_handler.write(b'AT&Q5\r\n')
        self.ser_handler.write(b'AT+MS=V34,1,0,33600,0,33600\r\n')
        # The modem responds to AT commands. Stores current modem settings
        self.ser_handler.write(b'AT%%DC0&W0\r\n')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        port = 'com5'

    fn = 'log_' + port
    myLogFormatter = logging.Formatter('[%(asctime)s | %(levelname)s] %(message)s')

    #handler settings
    myLogHandler = logging.handlers.TimedRotatingFileHandler(filename=fn+'.log', when='midnight', interval=1, encoding='utf-8')
    myLogHandler.setFormatter(myLogFormatter)
    myLogHandler.suffix = "%Y%m%d"

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(myLogFormatter)

    #logger set
    myLogger = logging.getLogger()
    myLogger.setLevel(logging.DEBUG)
    myLogger.addHandler(myLogHandler)
    myLogger.addHandler(streamHandler)

#    print('COM Port = ' + port)
    ser = SerialComm(port , 1200, myLogger)
    ser.open()
    while True:
        pass