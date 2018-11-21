# -*- coding: utf-8 -*-
import os
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow
from preference import Preference


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.clicked_fileOpen)
        self.actionSettings.triggered.connect(self.clicked_settings)
        self.filepath = None
        self.filename = None

    def clicked_fileOpen(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        openfile, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "All files (*.*);;CSV Files (*.csv)", options=options)
        if openfile:
            _, ext = os.path.splitext(openfile[0])
            self.filepath = openfile[0]
            self.filename = os.path.basename(openfile[0])
            if ext.lower() != '.csv' and ext.lower() != '.xlsx':
                QMessageBox.warning(self, "warning", "File extension error")
                self.filepath = None
                self.filename = None
            else:
                self.clicked_settings()

    def clicked_settings(self):
        self.dlg = Preference()
        self.dlg.le_file.setText(self.filepath)
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
