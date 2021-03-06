# -*- coding: utf-8 -*-
"""
Created on Sun May 20 11:35:03 2018

@author: DanielM
"""

import os
import numpy as np
import shelve

# Setup some parameters given by paradigm_frequency_inhibition.py
stim_delay = 100  # ms
dt = 0.01  # ms
stim_dtp = stim_delay / dt

data_path = "C:\\Users\\Daniel\\pyDentateData\\tuning\\revised\\spatial_inhibition_data\\globalrev\\"
save_path = data_path
data_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) and '.pydd' in f and not '.npz' in f]

for x in data_files:
    data = shelve.open(data_path + x)
    split_name_current = x.split('.')
    split_name_peaks = list(split_name_current)
    split_name_current[1] = split_name_current[1] + '_current'
    split_name_peaks[1] = split_name_peaks[1] + '_peaks'
    name_current = '.'.join(split_name_current)
    name_peaks = '.'.join(split_name_peaks)
    np.savez(save_path + name_current, np.array(data[data.keys()[0]]['populations'][0]['VClamps_i']))
        