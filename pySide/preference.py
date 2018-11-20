# -*- coding: utf-8 -*-

from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from ui_preference import Ui_Preference


class Preference(QDialog, Ui_Preference):
    def __init__(self):
        QDialog.__init__(self)
        Ui_Preference.__init__(self)
        self.str_locale = ["Colombia", "Turkey", "Korea"]
        self.str_dtformat = ["%d.%m.%Y %H:%M:%S", "%Y-%m-%d %H.%M.%S.%f", "%Y-%m-%d %H:%M:%S"]
        self.locale_index = 0
        self.setupUi(self)
        self.addUi()
        self.pb_cancel.clicked.connect(self.reject)
        self.pb_ok.clicked.connect(self.accept)

    def addUi(self):
        pixmap = QPixmap(":/bkground/images/Header.png")
        smaller_pixmap = pixmap.scaled(400, 80, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.lb_image.setPixmap(smaller_pixmap)
        self.lb_image.setScaledContents(True)

        self.cb_locale.addItems(self.str_locale)
        self.cb_datetime.addItems(self.str_dtformat)
        self.cb_locale.currentIndexChanged.connect(self.cb_locale_currentIndexChanged)

    def cb_locale_currentIndexChanged(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Preference()
    w.show()
    sys.exit(app.exec_())
    