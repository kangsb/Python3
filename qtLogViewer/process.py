#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class DataProcess:
    def __init__(self, filename, sep=',', dec='.', quot='"'):
        self.sep = sep
        self.dec = dec
        self.quot = quot
        self.filename = filename
        fn, ext = os.path.splitext(filename)
        print('fn = ' + fn)
        print('ext = ' + ext)
        if ext.upper() == '.CSV':
            print('csv file')
        elif ext.upper() == '.XLSX':
            print('xlsx file')
        else:
            print('unknown file')
    
    def openCSV(self, filename):
        self.df = pd.read_csv(filename, sep=self.sep, quotechar=self.quot, decimal=self.dec)
        return self.df.col

    def openXlsx(self, filename):
        self.df = pd.read_excel(filename)
        return self.df.col

    

    