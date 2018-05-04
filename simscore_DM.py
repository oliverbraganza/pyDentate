# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 15:23:42 2017

Original from Yim et al. 2015.
Modified to use the .npz file system instead of the .txt from Yim.
"""

import numpy as np
import pylab
from scipy.signal import correlate2d, convolve2d
from burst_generator_inhomogeneous_poisson import inhom_poiss
import shelve

def sim_score(signal1, signal2, kernel_delta):
    """Calculate the similatiry score as in Yim et al. 2015
    
    Parameters
    ----------
    signal1, signal2 - numpy arrays
        the two signals to be correlated
    kernal_delta - numeric
        the size of the triangular kernel in datapoints
        

    Returns
    -------
    corr - correlation coefficient
    """
    kernel = np.append(np.arange(kernel_delta),np.arange(kernel_delta,-1,-1))
    if np.shape(signal1) == np.shape(signal2):
        kernel=np.repeat(kernel[np.newaxis,:], repeats=np.shape(signal1)[0], axis=0)
    else:
        raise ValueError("signal1 and signal2 must have same shape")
    signal1_conv = convolve2d(signal1,kernel,'same')
    signal2_conv = convolve2d(signal2,kernel,'same')
    return signal1_conv

def time_stamps_to_signal(time_stamps, dt_signal, t_start, t_stop):
    """Convert an array of timestamps to a signal where 0 is absence and 1 is
    presence of spikes
    
    Parameters
    ----------
    time_stamps - numpy array
        the time stamps array to convert
    dt_signal - numeric
        the size of the triangular kernel in datapoints, units must be
        consistent with time_stamps
    t_start - numeric
        time where the signal starts, units must be consistent with time_stamps        
    t_stop - numeric
        time where the signal stops, units must be consistent with time_stamps

    Returns
    -------
    sig - correlation coefficient
    """
    # Construct a zero array with size corresponding to desired output signal
    sig = np.zeros((np.shape(time_stamps)[0],int((t_stop-t_start)/dt_signal)))
    
    # Find the indices where spikes occured according to time_stamps
    time_idc = (time_stamps - t_start) / dt_signal
    
    # Set the spike indices to 1
    for sig_idx, idc in enumerate(time_idc):
        sig[sig_idx,np.array(idc,dtype=np.int)] = 1

    return sig


if __name__ == '__main__':
    temporal_patterns = inhom_poiss()
    time_sig = time_stamps_to_signal(temporal_patterns,
                                     dt_signal=0.1,
                                     t_start=0,
                                     t_stop=1000)
    
    