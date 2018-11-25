# -*- coding: utf-8 -*-
"""MDI child class.
"""
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QWidget, QSizePolicy, QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from PySide2.QtCharts import QtCharts


class MdiChild(QWidget):
    """
    MDI child class
    """
    sequenceNumber = 1

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        hlayout = QHBoxLayout()
#        m = PlotCanvas(self, width=6, height=4)
#        m.move(0, 0)

        series = QtCharts.QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        chartView = QtCharts.QChartView()
        chartView.chart().addSeries(series)
        chartView.chart().createDefaultAxes()
        chartView.show()
        hlayout.addWidget(chartView)
        self.setLayout(hlayout)
        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MdiChild()
    sys.exit(app.exec_())
