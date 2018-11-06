#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import qdarkstyle
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
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt

class MyApp(QDialog):
    select_on_mouse_press = None

    def __init__(self):
        super().__init__()
        self.title = 'http://www.mopiens.com'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 480
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
#        self.statusBar().showMessage('Message in statusbar.')
        self.setWindowIcon(QIcon('res/app.png'))

        app = QCoreApplication.instance()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#        app.setStyleSheet(open("style.qss", "r").read())    
    
        self.imgLabel = QLabel(self)
        pixmap = QPixmap('res/app.png')
        resize_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imgLabel.setPixmap(resize_pixmap)

        self.btnQuit = QPushButton('Quit', self)
#        self.btnQuit.move(50, 50)
#        self.btnQuit.resize(self.quitButton.sizeHint())
        self.btnQuit.clicked.connect(QCoreApplication.instance().quit)

        stl = """QPushButton {
            background-color: #179AE0;
            border: 1px solid #31363B;
            color: #EFF0F1;
            border-radius: 4px;
            padding: 3px;
            outline: none;
        }
        QPushButton:hover {
            background: #179AE0;
            border: 1px solid #31363B;
            color: #31363B;
        }"""

        self.btnOk = QPushButton('Make graph', self)
        self.btnOk.setStyleSheet(open("style.qss", "r").read())
#        self.btnOk.move(50, 100)
#        self.btnOk.resize(self.okButton.sizeHint())

        self.leSep = QLineEdit()
        self.leSep.setPlaceholderText("Delimiter to use. Default ,(comma)")
        self.leQuote = QLineEdit()
        self.leQuote.setPlaceholderText("""The character used to denote the start and end of a quoted item. default "(Double quote) """)
        self.leDecimal = QLineEdit()
        self.leDecimal.setPlaceholderText("Decimal point. Default .(dot)")

        self.leFile = QLineEdit()
        self.leFile.setPlaceholderText("Select .csv or .xlsx")
        self.btnFile = QPushButton("Choose", self)

        fileOpenLayout = QHBoxLayout()
        fileOpenLayout.setSpacing(0)
        fileOpenLayout.setContentsMargins(0, 0, 0, 0)
        fileOpenLayout.addWidget(self.leFile)
        fileOpenLayout.addWidget(self.btnFile)

        propLayout = QGridLayout()
        propLayout.setAlignment(Qt.AlignCenter)
        propLayout.addWidget(QLabel("File:"), 0, 0)
        propLayout.addWidget(QLabel("Seperator:"), 1, 0)
#        propLayout.addWidget(QLabel("Quote character:"), 1, 0)
        propLayout.addWidget(QLabel("Decimal:"), 2, 0)

        propLayout.addLayout(fileOpenLayout, 0, 1)
        propLayout.addWidget(self.leSep, 1, 1)
#        propLayout.addWidget(self.leQuote, 1, 1)
        propLayout.addWidget(self.leDecimal, 2, 1)

        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addLayout(propLayout)
        mainLayout.addWidget(self.btnOk)
        mainLayout.addWidget(self.btnQuit)
        self.setLayout(mainLayout)
        self.show()

    def focusInEvent(self, ev):
        self.select_on_mouse_press = time.time()
        return QLineEdit.focusInEvent(self, ev)

    def mousePressEvent(self, ev):
        QLineEdit.mousePressEvent(self, ev)
        if self.select_on_mouse_press is not None and abs(time.time() - self.select_on_mouse_press) < 0.2:
            print('clicked')
        self.select_on_mouse_press = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
