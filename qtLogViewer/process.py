#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

class DataProcess:
    def __init__(self, filename, sep=',', dec='.', quot='"'):
        self.sep = sep
        self.dec = dec
        self.quot = quot
        self.filename = filename

    def fileOpen(self):
        _, ext = os.path.splitext(self.filename)
        if ext.lower() == '.csv':
            return self.openCSV()
        elif ext.lower() == '.xlsx':
            return self.openXlsx()
        else:
            print('unknown file')

    def openCSV(self):
        self.df = pd.read_csv(self.filename, sep=self.sep, quotechar=self.quot, decimal=self.dec, low_memory=False)
        return self.df.columns.tolist()

    def openXlsx(self):
        self.df = pd.read_excel(self.filename)
        return self.df.columns.tolist()

if __name__ == '__main__':
    dp = DataProcess('sample.csv')
    dp.fileOpen()

    

    