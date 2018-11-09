#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
"""

from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer
import sys

class ProgressDialog(QWidget):    
    def __init__(self):
        super().__init__()
        self.initUI()
                
    def initUI(self):      
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 10, 400, 5)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(0)
        self.setWindowTitle('QProgressBar')
        self.adjustSize()

        self.show()
            
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ProgressDialog()
    sys.exit(app.exec_())