# -*- coding: utf-8 -*-
import os
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from ui_preference import Ui_Preference


class Preference(QDialog, Ui_Preference):
    def __init__(self):
        QDialog.__init__(self)
        Ui_Preference.__init__(self)
        self.str_locale = ["Colombia", "Turkey", "Korea"]
        self.str_dtformat = ["%d.%m.%Y %H:%M:%S", "%Y-%m-%d %H.%M.%S.%f", "%Y-%m-%d %H:%M:%S"]
        self.str_seperator = [",", ",", ","]
        self.str_decimal = [",", ",", "."]
        self.locale_index = 0
        self.setupUi(self)
        self.addUi()
        self.pb_cancel.clicked.connect(self.reject)
        self.pb_ok.clicked.connect(self.accept)
        self.tb_open.clicked.connect(self.tb_open_clicked)

    def addUi(self):
        pixmap = QPixmap(":/bkground/images/Header.png")
        smaller_pixmap = pixmap.scaled(400, 80, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.lb_image.setPixmap(smaller_pixmap)
        self.lb_image.setScaledContents(True)

        self.cb_locale.addItems(self.str_locale)
        self.cb_datetime.addItems(self.str_dtformat)
        self.cb_locale.currentIndexChanged.connect(self.cb_locale_currentIndexChanged)
        self.cb_locale_currentIndexChanged()

    def cb_locale_currentIndexChanged(self):
        self.locale_index = self.cb_locale.currentIndex()
        self.cb_datetime.setCurrentIndex(self.locale_index)
        self.le_decimal.setText(self.str_decimal[self.locale_index])
        self.le_seperator.setText(self.str_seperator[self.locale_index])

    def tb_open_clicked(self):
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
                self.le_file.setText(self.filepath)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Preference()
    w.show()
    sys.exit(app.exec_())
    