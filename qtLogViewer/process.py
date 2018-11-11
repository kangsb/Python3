#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs

from PyQt5.QtCore import QObject, pyqtSignal
import weakref
import enum

@enum.unique
class EquipmentType(enum.Enum):
    LOC = 1
    GP  = 2
    DME = 3
    VOR = 4


class DataProcess(QObject):
    def __init__(self, filename, sep=',', dec='.', quot='"', datetime=None):
        super().__init__()
        self.sep = sep
        self.dec = dec
        self.quot = quot
        self.filename = filename
        self.datetime_format = datetime
        self.equipment = EquipmentType.DME

    def printProgress(self, str):
        pass

    def fileOpen(self):
        _, ext = os.path.splitext(self.filename)
        if ext.lower() == '.csv':
            self.df = pd.read_csv(self.filename, sep=self.sep, quotechar=self.quot, decimal=self.dec, low_memory=False)
        elif ext.lower() == '.xlsx':
            self.df = pd.read_excel(self.filename)
        else:
            print('unknown file')
            return
        
        try:
            self.bDateTime = True
#            print(self.datetime_format)
            self.df['TS'] = self.df['TS'].map(lambda x: datetime.strptime(str(x), self.datetime_format))
        except:
            import sys
            self.bDateTime = False
            print("Unexpected error:", sys.exc_info()[0])
            self.df['TS'] = self.df.index

    def makeGraph(self, title, ts, *col_list):
        if self.bDateTime:
            f = figure(width=1000, height=500, x_axis_type="datetime", title=title)
        else:
            f = figure(width=1000, height=500, title=title)

        props = dict(line_width=1, line_alpha=0.7)
        
        tim = self.df[ts]

        labels  = []
        active  = []
        keys    = []
        args    = {}
        index   = 0
        code    = ""
        COLORS  = ['red', 'orange', 'green', 'blue', 'black']
        for col_str in col_list:
            keys.append("l%d" % index)
            args[keys[index]] = f.line(tim, self.df[col_str], color=COLORS[index], legend=col_str, **props)
            labels.append(col_str)
            active.append(index)
            code += "l%d.visible = %d in checkbox.active;\n" % (index, index)
            index += 1
    
        checkbox = CheckboxGroup(labels=labels, active=active, width=300)
        args['checkbox'] = checkbox
        checkbox.callback = CustomJS.from_coffeescript(args=args, code=code)

        if self.bDateTime:
            fActive = figure(width=1000, height=100, x_axis_type="datetime", y_range=(0, 1))
        else:
            fActive = figure(width=1000, height=100)
        fActive.line(tim, self.df['CURRENT_TX'], color='black', legend='Active Tx', **props)
        layout = column(checkbox, f, fActive)

        return layout

#        y1 = self.df[col_list[0]]
#        y2 = self.df[col_list[1]]
#        l0 = p.line(tim, y1, color=Viridis3[0], legend=col_list[0], **props)
#        l1 = p.line(tim, y2, color=Viridis3[1], legend=col_list[1], **props)
    
#        checkbox = CheckboxGroup(labels=labels, active=active, width=300)
#        checkbox.callback = CustomJS.from_coffeescript(args=dict(l0=linegraph[0], l1=linegraph[1], checkbox=checkbox), code="""
#        l0.visible = 0 in checkbox.active;
#        l1.visible = 1 in checkbox.active;
#        """)



if __name__ == '__main__':
    dp = DataProcess(filename='sample.csv', sep=',', dec=',')
    print('Program start...')
    dp.fileOpen()
    print('File opened.')
    tabs = dp.makeTabWidget()
    print('Tab generation finished.')
    show(tabs)

