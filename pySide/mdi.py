# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from PySide2.QtCore import QFile
from PySide2.QtCore import QFileInfo
from PySide2.QtCore import QPoint
from PySide2.QtCore import QSettings
from PySide2.QtCore import QSignalMapper
from PySide2.QtCore import QSize
from PySide2.QtCore import QTextStream
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QMdiArea
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QWidget

import mdi_rc


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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.window_mapper = QSignalMapper(self)
        self.window_mapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()
        self.setWindowTitle("MDI")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def createsChildWindow(self):
        self.mySubwindow = MdiChild()
        self.mySubwindow.createWindow(500, 400)
        self.mySubwindow.show()

    def newFile(self):
        self.createsChildWindow()
        #child = self.createMdiChild()
        #child.newFile()
        #child.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()

    def about(self):
        QMessageBox.about(
            self, "About MDI",
            "The <b>MDI</b> example demonstrates how to write multiple "
            "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

        hasSelection = (self.activeMdiChild() is not None and
                        self.activeMdiChild().textCursor().hasSelection())
        self.cutAct.setEnabled(hasSelection)
        self.copyAct.setEnabled(hasSelection)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.window_mapper.map)
            self.window_mapper.setMapping(action, window)

    def createMdiChild(self):
        child = MdiChild()
        self.mdiArea.addSubWindow(child)

        child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)

        return child

    def createActions(self):
        self.newAct = QAction(QIcon(
            ':/images/new.png'), "&New", self,
            shortcut=QKeySequence.New, statusTip="Create a new file",
            triggered=self.newFile)

        self.openAct = QAction(QIcon(
            ':/images/open.png'), "&Open...", self,
            shortcut=QKeySequence.Open, statusTip="Open an existing file",
            triggered=self.open)

        self.saveAct = QAction(QIcon(
            ':/images/save.png'), "&Save", self,
            shortcut=QKeySequence.Save,
            statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction(
            "Save &As...", self,
            shortcut=QKeySequence.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.saveAs)

        self.exitAct = QAction(
            "E&xit", self, shortcut=QKeySequence.Quit,
            statusTip="Exit the application",
            triggered=QApplication.instance().closeAllWindows)

        self.cutAct = QAction(
            QIcon(':/images/cut.png'), "Cu&t", self,
            shortcut=QKeySequence.Cut,
            statusTip="Cut the current selection's contents to the clipboard",
            triggered=self.cut)

        self.copyAct = QAction(
            QIcon(':/images/copy.png'), "&Copy", self,
            shortcut=QKeySequence.Copy,
            statusTip="Copy the current selection's contents to the clipboard",
            triggered=self.copy)

        self.pasteAct = QAction(
            QIcon(':/images/paste.png'), "&Paste", self,
            shortcut=QKeySequence.Paste,
            statusTip="Paste the clipboard's contents into the current selection",
            triggered=self.paste)

        self.closeAct = QAction(
            "Cl&ose", self,
            statusTip="Close the active window",
            triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction(
            "Close &All", self,
            statusTip="Close all the windows",
            triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction(
            "&Tile", self, statusTip="Tile the windows",
            triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction(
            "&Cascade", self,
            statusTip="Cascade the windows",
            triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction(
            "Ne&xt", self, shortcut=QKeySequence.NextChild,
            statusTip="Move the focus to the next window",
            triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction(
            "Pre&vious", self,
            shortcut=QKeySequence.PreviousChild,
            statusTip="Move the focus to the previous window",
            triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction(
            "&About", self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self.aboutQtAct = QAction(
            "About &Qt", self,
            statusTip="Show the Qt library's About box",
            triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        action = self.fileMenu.addAction("Switch layout direction")
        action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
