#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.palettes import Viridis3
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
        output_file("line_on_off.html", title="line_on_off.py example")

        source = ColumnDataSource(self.df)
        p = figure(x_axis_type="datetime", title="Stock Closing Price")
        props = dict(line_width=4, line_alpha=0.7)
#        datetime_format = r'%d.%m.%Y %H:%M:%S'
#        ts = self.df['TS'].map(lambda x: datetime.strptime(str(x), datetime_format))
        ts = self.df['TS']
#        ts = ColumnDataSource(self.df['TS'])
#        print(ts.head())
        y1 = self.df[col_list[0]]
        y2 = self.df[col_list[1]]

        l0 = p.line(ts, y1, color=Viridis3[0], legend=col_list[0], **props)
        l1 = p.line(ts, y2, color=Viridis3[1], legend=col_list[1], **props)
#        l0 = p.line((list(self.df['TS'])), list(self.df[col_list[0]]), color=Viridis3[0], legend=col_list[0], **props)
#        l1 = p.line((list(self.df['TS'])), list(self.df[col_list[0]]), color=Viridis3[1], legend=col_list[1], **props)

        desc = self.df[col_list[0]].describe()
        print(desc)

        checkbox = CheckboxGroup(labels=[col_list[0], col_list[1]],
                                active=[0, 1], width=100)
        checkbox.callback = CustomJS.from_coffeescript(args=dict(l0=l0, l1=l1, checkbox=checkbox), code="""
        l0.visible = 0 in checkbox.active;
        l1.visible = 1 in checkbox.active;
        """)
        layout = row(checkbox, p)
        show(layout)

if __name__ == '__main__':
    dp = DataProcess('sample.csv')
    dp.fileOpen()
    dp.makeGraph('TS', 'MON1_TX1_PULSE_RISE_TIME', 'MON2_TX1_PULSE_RISE_TIME')
    

    