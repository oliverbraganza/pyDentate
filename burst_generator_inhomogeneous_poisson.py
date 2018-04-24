# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:37:20 2018

@author: DanielM
"""

import numpy as np
import matplotlib.pyplot as plt
from elephant import spike_train_generation
from neo.core import AnalogSignal
import quantities as pq

# Generate as rate profile for the inhomogeneous_poisson_process
def inhom_poiss():
    
    t_start = 0 * pq.s
    t_stop = 0.5 * pq.s
    sampling_interval = 0.0001 * pq.s
    max_rate = 100
    
    t = np.arange(0,0.5,sampling_interval.magnitude)
    
    rate_profile = (np.sin(t*10*np.pi*2-np.pi/2) + 1) * max_rate / 2

    rate_profile_as_asig = AnalogSignal(rate_profile, units = 1*pq.Hz,t_start=0*pq.s, t_stop=0.5*pq.s, sampling_period = sampling_interval)

    what = []
    for x in range(400):
        what.append(spike_train_generation.inhomogeneous_poisson_process(rate_profile_as_asig))

    array_like = np.array([np.array(x.times)*1000 for x in what])

    return array_like

if __name__ == "__main__":
    result = inhom_poiss()
    plt.eventplot(result)
"""
temporal_patterns = poisson_burst_generator(inter_burst_interval=100,
                                           nr_bursts=20,
                                           nr_trains=1000,
                                           intra_burst_interval=100,
                                           spikes_per_burst=3,
                                           numpy_seed=10001,
                                           train_t_stop=1000,
                                           burst_t_stop=None)
plt.figure()
plt.eventplot(temporal_patterns)
plt.title("numpy generated eventplot")

plt.figure()
plt.hist(np.hstack(np.array(temporal_patterns).flat), bins = int(np.hstack(np.array(temporal_patterns).flat).max()))
plt.title("numpy generated time histogram")

isis=[]
for x in temporal_patterns:
    curr = np.diff(x)
    isis.extend(curr)
plt.figure()
isis = np.array(isis)
plt.hist(isis, bins=int(round(isis.max()/0.1)))
"""