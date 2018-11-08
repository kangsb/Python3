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
from bokeh.models.widgets import Panel, Tabs
import enum

@enum.unique
class EquipmentType(enum.Enum):
    LOC = 1
    GP  = 2
    DME = 3
    VOR = 4


class DataProcess:
    def __init__(self, filename, sep=',', dec='.', quot='"'):
        self.sep = sep
        self.dec = dec
        self.quot = quot
        self.filename = filename
        self.equipment = EquipmentType.DME

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

        f = figure(width=1000, height=500, x_axis_type="datetime", title=None)
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

    def makeTabWidget(self):
        layout = self.makeGraph('TS', 'MON1_TX1_PULSE_RISE_TIME', 'MON2_TX1_PULSE_RISE_TIME', 'MON1_TX2_PULSE_RISE_TIME', 'MON2_TX2_PULSE_RISE_TIME')
        tab1 = Panel(child=layout, title="Rise Time")
        print('Tab1 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_PULSE_DECAY_TIME', 'MON2_TX1_PULSE_DECAY_TIME', 'MON1_TX2_PULSE_DECAY_TIME', 'MON2_TX2_PULSE_DECAY_TIME')
        tab2 = Panel(child=layout, title="Decay Time")
        print('Tab2 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_PULSE_DURATION', 'MON2_TX1_PULSE_DURATION', 'MON1_TX2_PULSE_DURATION', 'MON2_TX2_PULSE_DURATION')
        tab3 = Panel(child=layout, title="Duration")
        print('Tab3 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_PULSE_SPACING', 'MON2_TX1_PULSE_SPACING', 'MON1_TX2_PULSE_SPACING', 'MON2_TX2_PULSE_SPACING')
        tab4 = Panel(child=layout, title="Spacing")
        print('Tab4 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_TIME_DELAY', 'MON2_TX1_TIME_DELAY', 'MON1_TX2_TIME_DELAY', 'MON2_TX2_TIME_DELAY')
        tab5 = Panel(child=layout, title="Delay")
        print('Tab5 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_TRANSMISSION_RATE', 'MON2_TX1_TRANSMISSION_RATE', 'MON1_TX2_TRANSMISSION_RATE', 'MON2_TX2_TRANSMISSION_RATE')
        tab6 = Panel(child=layout, title="Transmit Rate")
        print('Tab6 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_REPLY_EFFICIENCY', 'MON2_TX1_REPLY_EFFICIENCY', 'MON1_TX2_REPLY_EFFICIENCY', 'MON2_TX2_REPLY_EFFICIENCY')
        tab7 = Panel(child=layout, title="Efficiency")
        print('Tab7 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_PEAK_POWER_OUTPUT', 'MON2_TX1_PEAK_POWER_OUTPUT', 'MON1_TX2_PEAK_POWER_OUTPUT', 'MON2_TX2_PEAK_POWER_OUTPUT')
        tab8 = Panel(child=layout, title="Ouput Power")
        print('Tab8 finished...')
        layout = self.makeGraph('TS', 'MON1_TX1_FREQUENCY', 'MON2_TX1_FREQUENCY', 'MON1_TX2_FREQUENCY', 'MON2_TX2_FREQUENCY')
        tab9 = Panel(child=layout, title="Frequency")
        print('Tab9 finished...')

        tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9])
        return tabs


if __name__ == '__main__':
    dp = DataProcess(filename='sample.csv', sep=',', dec=',')
    print('Program start...')
    dp.fileOpen()
    print('File opened.')
    tabs = dp.makeTabWidget()
    print('Tab generation finished.')
    show(tabs)

