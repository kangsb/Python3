# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QDialog, QMessageBox, QMainWindow
from ui_mainwindow import Ui_MainWindow
from preference import Preference

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.clicked_fileOpen)
    
    def clicked_fileOpen(self):
        """        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()
        """
        self.dlg = Preference()
#        self.dlg.show()
        res = self.dlg.exec_()
        if res == QDialog.Accepted:
            print("Accepted")
        else:
            print("Rejected")
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    