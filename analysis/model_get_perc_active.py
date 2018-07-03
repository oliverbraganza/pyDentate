# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 10:25:41 2018

@author: daniel
"""
import shelve
import numpy as np
import matplotlib.pyplot as plt
import os

#Home PC
#directory = "C:\\Users\\daniel\\repos\\pyDentate\paradigm_pattern-separation_saves_2018-03-11\\"
#Office PC
#directory = "Y:\\DanielM\\023_Dentate Gyrus Model\\paradigm_spatial-inhibition\\"
#Dropbox
data_path = "C:\\Users\\Daniel\\pyDentateData\\pattern_separation_data_rate\\net_globalrev_030\\"
file_name = "net_globalrev.TunedNetwork_data_paradigm_rate-pattern-separation_run_scale_seed_000_030_0.pydd"
data_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) and '.pydd' in f and not '.npz' in f]
data_files.sort()

data = shelve.open(data_path + file_name)
perc_active_gcs_list = []
perc_active_mcs_list = []
perc_active_bcs_list = []
perc_active_hcs_list = []

n_aps_avg_gcs_list = []
n_aps_avg_mcs_list = []
n_aps_avg_bcs_list = []
n_aps_avg_hcs_list = []

n_aps_std_gcs_list = []
n_aps_std_mcs_list = []
n_aps_std_bcs_list = []
n_aps_std_hcs_list = []

# Get to BasketCell Connection
for x in data_files:
    curr_data = shelve.open(data_path + x)
    active_gcs = np.array(np.argwhere(np.array(curr_data[curr_data.keys()[0]]['populations'][0]['ap_number']) > 0),dtype = int).flatten()
    active_mcs = np.array(np.argwhere(np.array(curr_data[curr_data.keys()[0]]['populations'][1]['ap_number']) > 0),dtype = int).flatten()
    active_bcs = np.array(np.argwhere(np.array(curr_data[curr_data.keys()[0]]['populations'][2]['ap_number']) > 0),dtype = int).flatten()
    active_hcs = np.array(np.argwhere(np.array(curr_data[curr_data.keys()[0]]['populations'][3]['ap_number']) > 0),dtype = int).flatten()

    n_aps_avg_gcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][0]['ap_number'])[active_gcs].mean())
    n_aps_std_gcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][0]['ap_number'])[active_gcs].std())

    n_aps_avg_mcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][1]['ap_number'])[active_mcs].mean())
    n_aps_std_mcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][1]['ap_number'])[active_mcs].std())

    n_aps_avg_bcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][2]['ap_number'])[active_bcs].mean())
    n_aps_std_bcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][2]['ap_number'])[active_bcs].std())
    
    n_aps_avg_hcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][3]['ap_number'])[active_hcs].mean())
    n_aps_std_hcs_list.append(np.array(curr_data[curr_data.keys()[0]]['populations'][3]['ap_number'])[active_hcs].std())

    perc_active_gcs_list.append((len(active_gcs) / 2000.0)*100)
    perc_active_mcs_list.append((len(active_mcs) / 60.0)*100)
    perc_active_bcs_list.append((len(active_bcs) / 24.0)*100)
    perc_active_hcs_list.append((len(active_hcs) / 24.0)*100)
    
n_active_gcs_array = np.array(perc_active_gcs_list)
n_active_mcs_array = np.array(perc_active_mcs_list)
n_active_bcs_array = np.array(perc_active_bcs_list)
n_active_hcs_array = np.array(perc_active_hcs_list)