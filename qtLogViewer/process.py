#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.plotting import figure, ColumnDataSource

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
        self.df = pd.read_csv(self.filename, sep=self.sep, quotechar=self.quot, decimal=self.dec, low_memory=False, parse_dates=[0])
        return self.df.columns.tolist()

    def openXlsx(self):
        self.df = pd.read_excel(self.filename)
        return self.df.columns.tolist()

    def makeGraph(self, ts, *col_list):
        output_file("output.html", title="example")

        f = figure(x_axis_type="datetime")
        props = dict(line_width=2, line_alpha=0.7)
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
        layout = row(checkbox, f)
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
    dp.fileOpen()
    layout = dp.makeGraph('TS', 'MON1_TX1_TIME_DELAY', 'MON2_TX1_TIME_DELAY', 'MON1_TX2_TIME_DELAY', 'MON2_TX2_TIME_DELAY')
    show(layout)

