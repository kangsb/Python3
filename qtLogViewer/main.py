#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import qdarkstyle
from progressThread import *
from process import DataProcess
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QProgressBar

from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtCore import QThread

from bokeh.io import output_file, show


class MyApp(QDialog):
    fileName = None

    def __init__(self):
        super().__init__()
        self.title = 'Log Viewer'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 480
        self.initUI()
        self.initProgressBar()

    def initProgressBar(self):
        self.pgsb = QProgressBar()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
#        self.statusBar().showMessage('Message in statusbar.')
        self.setWindowIcon(QIcon('res/app.png'))

        app = QCoreApplication.instance()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#        app.setStyleSheet(open("style.qss", "r").read())    
    
        fontTitle = QFont("Tahoma", 14, QFont.Bold) 
        fontText = QFont("Tahoma", 10, QFont.Normal) 
        self.setFont(fontText)

        self.lbImage = QLabel(self)
        pixmap = QPixmap('res/app.png')
        resize_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.lbImage.setPixmap(resize_pixmap)
        self.lbDesc = QLabel('Quintet log file viewer', self)
        self.lbDesc.setFont(fontTitle)

        self.leFile = QLineEdit()
        self.leFile.setPlaceholderText("Select .csv or .xlsx")
        self.leFile.setFont(fontText)

        self.btnFile = QPushButton("Choose", self)
        self.btnFile.clicked.connect(self.btnFile_clicked)

        lbFile = QLabel("File:", self)
        lbSep = QLabel("Seperator:", self)
        lbDec = QLabel("Decimal:", self)
        self.leSep = QLineEdit()
        self.leSep.setFont(fontText)
        self.leSep.setPlaceholderText("Delimiter to use. Default ,(comma)")
        self.leDecimal = QLineEdit()
        self.leDecimal.setFont(fontText)
        self.leDecimal.setPlaceholderText("Decimal point. Default .(dot)")

        self.btnOk = QPushButton('Make graph', self)
        self.btnOk.setStyleSheet(open("mystyle.qss", "r").read())
        self.btnOk.clicked.connect(self.btnOk_clicked)

        self.btnQuit = QPushButton('Quit', self)
        self.btnQuit.clicked.connect(QCoreApplication.instance().quit)

        descLayout = QHBoxLayout()
        descLayout.setAlignment(Qt.AlignLeft)
        descLayout.setSpacing(10)
        descLayout.setContentsMargins(10, 10, 10, 10)
        descLayout.addWidget(self.lbImage)
        descLayout.addWidget(self.lbDesc)
        
        fileOpenLayout = QHBoxLayout()
        fileOpenLayout.setSpacing(10)
        fileOpenLayout.setContentsMargins(0, 0, 0, 0)
        fileOpenLayout.addWidget(self.leFile)
        fileOpenLayout.addWidget(self.btnFile)

        propLayout = QGridLayout()
        propLayout.setAlignment(Qt.AlignCenter)
        propLayout.setSpacing(10)
        propLayout.setContentsMargins(0, 0, 0, 0)
        propLayout.addWidget(lbFile, 0, 0)
        propLayout.addWidget(lbSep, 1, 0)
        propLayout.addWidget(lbDec, 2, 0)
        propLayout.addLayout(fileOpenLayout, 0, 1)
        propLayout.addWidget(self.leSep, 1, 1)
        propLayout.addWidget(self.leDecimal, 2, 1)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.addLayout(descLayout)
        mainLayout.addLayout(propLayout)
        mainLayout.addWidget(self.btnOk)
        mainLayout.addWidget(self.btnQuit)
        self.setLayout(mainLayout)
        self.adjustSize()
        self.show()

#    def focusInEvent(self, ev):
#        self.select_on_mouse_press = time.time()
#        QLineEdit.focusInEvent(self, ev)

#    def mousePressEvent(self, ev):
#        self.leFile.mousePressEvent(self, ev)
#        if self.select_on_mouse_press is not None and abs(time.time() - self.select_on_mouse_press) < 0.2:
#        QMessageBox.about(self, "message", "clicked")
#        self.select_on_mouse_press = None

    def btnFile_clicked(self):
        options = QFileDialog.Options()
#        options |= QFileDialog.DontUseNativeDialog
        openFileName = QFileDialog.getOpenFileName(self, 'Open file', "", "All Files (*);;csv File (*.csv);;xlsx File (*.xlsx)", options=options)
        if openFileName != ('', ''):
            _, ext = os.path.splitext(openFileName[0])
            if ext.lower() != '.csv' and ext.lower() != '.xlsx':
                QMessageBox.warning(self, "warning", "File extension error")
                self.fileName = None
            else:
                self.fileName = openFileName[0]
                self.leFile.setText(openFileName[0])
 
    def btnOk_clicked(self):
        if self.fileName == None:
            QMessageBox.warning(self, "warning", "Please select a file")
        else:
            sep = self.leSep.text()
            sep = sep.replace(" ", "") 
            dec = self.leDecimal.text()
            dec = dec.replace(" ", "") 

            sep = ',' if len(sep) == 0 else sep
            dec = '.' if len(dec) == 0 else dec
            print('sec = ' + sep + ', dec = ' + dec)
            dp = DataProcess(filename=self.fileName, sep=sep, dec=dec, quot='"')
            print('Program start...')
            dp.fileOpen()
            print('File opened.')
            tabs = dp.makeTabWidget()
            print('Tab generation finished.')
            show(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
