#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import qdarkstyle

from process import DataProcess
from process import EquipmentType
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QComboBox
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
from PyQt5.QtCore import pyqtSlot

from bokeh.io import output_file, show
from bokeh.models.widgets import Panel, Tabs
from time import sleep

class MyApp(QWidget):
    fileName = None

    def __init__(self):
        super().__init__()
        self.title = 'Log Viewer'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 300
        self.initUI()

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

        equipLayout = QHBoxLayout()
        self.rbLoc = QRadioButton("LOC")
        self.rbLoc.setChecked(True)
        self.equipment = EquipmentType.LOC
        self.rbLoc.toggled.connect(lambda:self.radioState(self.rbLoc))
        self.rbGp = QRadioButton("GP")
        self.rbGp.toggled.connect(lambda:self.radioState(self.rbGp))
        self.rbDme = QRadioButton("DME")
        self.rbDme.toggled.connect(lambda:self.radioState(self.rbDme))
        equipLayout.addWidget(self.rbLoc)
        equipLayout.addWidget(self.rbGp)
        equipLayout.addWidget(self.rbDme)

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

        self.cbDateTimeFormat = QComboBox()
        self.cbDateTimeFormat.addItem('%d.%m.%Y %H:%M:%S')
        self.cbDateTimeFormat.addItem('%Y-%m-%d %H.%M.%S.%f')
        self.cbDateTimeFormat.setEditable(True)
#        self.cbDateTimeFormat.setPlaceholderText('date/time format string')
        self.cbDateTimeFormat.setCurrentIndex(-1)
        self.cbDateTimeFormat.currentTextChanged.connect(self.cbTextChanged)  # 현재 인덱스의 데이터가 바뀔 때

        propLayout = QGridLayout()
        propLayout.setAlignment(Qt.AlignCenter)
        propLayout.setSpacing(10)
        propLayout.setContentsMargins(0, 0, 0, 0)

        propLayout.addWidget(QLabel('Equipment:', self), 0, 0)
        propLayout.addWidget(QLabel('File:', self), 1, 0)
        propLayout.addWidget(QLabel('Seperator:', self), 2, 0)
        propLayout.addWidget(QLabel('Decimal:', self), 3, 0)
        propLayout.addWidget(QLabel('Date/Time format:', self), 4, 0)
        propLayout.addLayout(equipLayout, 0, 1)
        propLayout.addLayout(fileOpenLayout, 1, 1)
        propLayout.addWidget(self.leSep, 2, 1)
        propLayout.addWidget(self.leDecimal, 3, 1)
        propLayout.addWidget(self.cbDateTimeFormat, 4, 1)


        self.pbar = QProgressBar(self)
#        self.pbar.setGeometry(50, 10, 400, 5)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(0)
        self.pbar.setHidden(True)
        self.lbStatus = QLabel()
        self.lbStatus.setText('Ready')

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.addLayout(descLayout)
        mainLayout.addLayout(propLayout)
        mainLayout.addWidget(self.btnOk)
        mainLayout.addWidget(self.btnQuit)
        mainLayout.addWidget(self.pbar)
        mainLayout.addWidget(self.lbStatus)

        self.setLayout(mainLayout)

        self.setTabOrder(self.rbLoc, self.rbGp)
        self.setTabOrder(self.rbGp, self.rbDme)
        self.setTabOrder(self.rbDme, self.btnFile)
        self.setTabOrder(self.btnFile, self.leSep)
        self.setTabOrder(self.leSep, self.leDecimal)
        self.setTabOrder(self.leDecimal, self.cbDateTimeFormat)
        self.setTabOrder(self.cbDateTimeFormat, self.btnOk)
        self.setTabOrder(self.btnOk, self.btnQuit)

#        self.adjustSize()
        self.show()

    def cbTextChanged(self):
        pass

    def radioState(self, b):
        if b.text() == "LOC":
            if b.isChecked() == True:
                self.equipment = EquipmentType.LOC
        elif b.text() == "GP":
            if b.isChecked() == True:
                self.equipment = EquipmentType.GP
        elif b.text() == "DME":
            if b.isChecked() == True:
                self.equipment = EquipmentType.DME

    def btnFile_clicked(self):
        options = QFileDialog.Options()
#        options |= QFileDialog.DontUseNativeDialog
        openFileName = QFileDialog.getOpenFileName(self, 'Open file', "", "All Files (*);;csv File (*.csv);;xlsx File (*.xlsx)", options=options)
        if openFileName != ('', ''):
            _, ext = os.path.splitext(openFileName[0])
            self.baseName = os.path.basename(openFileName[0])
            if ext.lower() != '.csv' and ext.lower() != '.xlsx':
                QMessageBox.warning(self, "warning", "File extension error")
                self.fileName = None
            else:
                self.fileName = openFileName[0]
                self.leFile.setText(openFileName[0])
                self.setWindowTitle(self.baseName)
 
    def btnOk_clicked(self):
        if self.fileName == None:
            QMessageBox.warning(self, "warning", "Please select a file")
        else:
            self.mainProcess()

    def mainProcess(self):
        sep = self.leSep.text()
        sep = sep.replace(" ", "") 
        dec = self.leDecimal.text()
        dec = dec.replace(" ", "") 

        sep = ',' if len(sep) == 0 else sep
        dec = '.' if len(dec) == 0 else dec
        datetime = self.cbDateTimeFormat.currentText()
        datetime = None if len(datetime) == 0 else datetime
        self.dp = DataProcess(filename=self.fileName, sep=sep, dec=dec, quot='"', datetime=datetime)
        fn = self.baseName.split('.')
        outfile = fn[0] + '.html'
        output_file(outfile, title=outfile)

        self.lbStatus.setText('Opening file...')
        self.dp.fileOpen()
        if self.equipment == EquipmentType.LOC:
            self.makeLGTabbedHtml(self.equipment)
        elif self.equipment == EquipmentType.GP:
            self.makeLGTabbedHtml(self.equipment)
        elif self.equipment == EquipmentType.DME:
            self.makeDMETabbedHtml()
        else:
            self.lbStatus.setText('Equipment type error')
            return

        self.lbStatus.setText('Ready')

    def makeLGTabbedHtml(self, equip):
        __total = 9
        current = 1
        title = None
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CL SDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CL_SDM', 'MON2_CL_SDM')
        tab1 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CL_DDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CL_DDM', 'MON2_CL_DDM')
        tab2 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CL RF Level"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CL_RFLEVEL', 'MON2_CL_RFLEVEL')
        tab3 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "DS SDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_DS_SDM', 'MON2_DS_SDM')
        tab4 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "DS DDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_DS_DDM', 'MON2_DS_DDM')
        tab5 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "DS RF Level"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_DS_RFLEVEL', 'MON2_DS_RFLEVEL')
        tab6 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CLR SDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CLR_SDM', 'MON2_CLR_SDM')
        tab7 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CLR DDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CLR_DDM', 'MON2_CLR_DDM')
        tab8 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "CLR RF Level"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_CLR_RFLEVEL', 'MON2_CLR_RFLEVEL')
        tab9 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "NF SDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_NF_SDM', 'MON2_NF_SDM')
        tab10 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "NF DDM"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_NF_DDM', 'MON2_NF_DDM')
        tab11 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "NF RF Level"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_NF_RFLEVEL', 'MON2_NF_RFLEVEL')
        tab12 = Panel(child=layout, title=title)

        self.lbStatus.setText('Tab gernation all finished.\n')

        tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12])
        sleep(0.5)
        show(tabs)

    def makeDMETabbedHtml(self):
        __total = 9
        current = 1
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Rise Time"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_PULSE_RISE_TIME', 'MON2_TX1_PULSE_RISE_TIME', 'MON1_TX2_PULSE_RISE_TIME', 'MON2_TX2_PULSE_RISE_TIME')
        tab1 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Decay Time"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_PULSE_DECAY_TIME', 'MON2_TX1_PULSE_DECAY_TIME', 'MON1_TX2_PULSE_DECAY_TIME', 'MON2_TX2_PULSE_DECAY_TIME')
        tab2 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Duration"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_PULSE_DURATION', 'MON2_TX1_PULSE_DURATION', 'MON1_TX2_PULSE_DURATION', 'MON2_TX2_PULSE_DURATION')
        tab3 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Spacing"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_PULSE_SPACING', 'MON2_TX1_PULSE_SPACING', 'MON1_TX2_PULSE_SPACING', 'MON2_TX2_PULSE_SPACING')
        tab4 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Delay"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_TIME_DELAY', 'MON2_TX1_TIME_DELAY', 'MON1_TX2_TIME_DELAY', 'MON2_TX2_TIME_DELAY')
        tab5 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Transmit Rate"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_TRANSMISSION_RATE', 'MON2_TX1_TRANSMISSION_RATE', 'MON1_TX2_TRANSMISSION_RATE', 'MON2_TX2_TRANSMISSION_RATE')
        tab6 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Efficiency"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_REPLY_EFFICIENCY', 'MON2_TX1_REPLY_EFFICIENCY', 'MON1_TX2_REPLY_EFFICIENCY', 'MON2_TX2_REPLY_EFFICIENCY')
        tab7 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Ouput Power"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_PEAK_POWER_OUTPUT', 'MON2_TX1_PEAK_POWER_OUTPUT', 'MON1_TX2_PEAK_POWER_OUTPUT', 'MON2_TX2_PEAK_POWER_OUTPUT')
        tab8 = Panel(child=layout, title=title)
        self.lbStatus.setText('Create Tab{} ({}/{})...'.format(current, current, __total))
        current += 1
        title = "Frequency"
        layout = self.dp.makeGraph(title, 'TS', 'MON1_TX1_FREQUENCY', 'MON2_TX1_FREQUENCY', 'MON1_TX2_FREQUENCY', 'MON2_TX2_FREQUENCY')
        tab9 = Panel(child=layout, title=title)
        self.lbStatus.setText('Tab gernation all finished.\n')

        tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9])
        sleep(0.5)
        show(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
