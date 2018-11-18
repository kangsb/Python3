# -*- coding: utf-8 -*-
"""MDI child class.
"""
from PySide2.QtCore import QFile
from PySide2.QtCore import QFileInfo
from PySide2.QtCore import QTextStream
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QWidget


class MdiChild(QWidget):
    """
    MDI child class
    """
    sequenceNumber = 1

    def __init__(self):
        super(MdiChild, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.is_untitled = True
        self.cur_file = None

    def newFile(self):
        self.is_untitled = True
        self.cur_file = "document%d.txt" % MdiChild.sequenceNumber
        MdiChild.sequenceNumber += 1
        self.setWindowTitle(self.cur_file + '[*]')
        self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(
                self, "MDI", "Cannot read file %s:\n%s." %
                (fileName, file.errorString()))
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.document().contentsChanged.connect(self.documentWasModified)

        return True

    def save(self):
        if self.is_untitled:
            return self.saveAs()
        else:
            return self.saveFile(self.cur_file)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                  self.cur_file)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "MDI", "Cannot write file %s:\n%s." %
                                (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.cur_file)

    def currentFile(self):
        return self.cur_file

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.document().isModified():
            ret = QMessageBox.warning(
                self, "MDI",
                "'%s' has been modified.\nDo you want to save your "
                "changes?" % self.userFriendlyCurrentFile(),
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.cur_file = QFileInfo(fileName).canonicalFilePath()
        self.is_untitled = False
        self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()
