# -*- coding: utf-8 -*-
import thinkdsp
import thinkplot
import numpy as np
import warnings
warnings.filterwarnings('ignore')

cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)

cos_sig.plot()
#sin_sig.plot()
thinkplot.config(xlabel='Time (s)')