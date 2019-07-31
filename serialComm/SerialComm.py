# -*- coding:utf-8 -*-

import sys
import serial
import threading
from datetime import datetime, timedelta

class SerialComm:
    def __init__(self, port, baudrate):
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

    def open(self):
        self.ser_handler = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity)
#        self.modem_init()
        self._start_receiver()
        #self._start_sender()

    def _start_sender(self):
        """sender thread"""
        print('Sender thread now running')
        self.sender_thread = threading.Thread(target=self.sender, name='tx')
        self.sender_thread.daemon = True
        self.sender_thread.start()

    def _start_receiver(self):
        """receiver thread"""
        print('Receiver thread now running')
        self.reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_receiver(self):
        self.reader_alive = False
        self.receiver_thread.join()

    def reader(self):
        """loop and copy serial->console"""
        try:
            str_data = ''
            while self.ser_handler.is_open:
                # read all that is there or wait for one byte
                data = self.ser_handler.read(1) #(self.ser_handler.in_waiting or 1)
                if data:
                    hex_string = data.hex() #binascii.hexlify(data).decode('utf-8')
                    if hex_string == '11':
                        str_data += '\n'
                        dt = datetime.now()
                        fn = dt.strftime('%Y%m%d-%H.txt')
                        tm = dt.strftime('%H:%M:%S, ')
                        with open(fn, "a") as f:
                            f.write(tm)
                            f.write(str_data)
                            print(tm + str_data, end='')
                            str_data = ''
                    str_data += (hex_string + ' ')

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
    ser = SerialComm('COM10', 1200)
    ser.open()
    while True:
        pass