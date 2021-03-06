# -*- coding: utf-8 -*-
"""
This module implements the class StandardNetwork.
StandardNetwork creates a ring network as defined in Santhakumar et al. 2005
with some changes as in Yim et al. 2015.
See StandardNetwork docstring for details.
Created on Tue Nov 28 13:01:38 2017

@author: DanielM
"""

from neuron import h, gui
import ouropy
import matplotlib.pyplot as plt
import numpy as np
from granulecell import GranuleCell
from mossycell_cat import MossyCell
from basketcell import BasketCell
from hippcell import HippCell

class TunedNetwork(ouropy.gennetwork.GenNetwork):
    """ This model implements the ring model from Santhakumar et al. 2005.
    with some changes as in Yim et al. 2015.
    It features inhibition but omits the MC->GC connection.
    """
    name = "TunedNetwork"

    def __init__(self, seed=None, temporal_patterns=np.array([]),
                 spatial_patterns_gcs=np.array([]),
                 spatial_patterns_bcs=np.array([])):
        self.init_params = locals()
        self.init_params['self'] = str(self.init_params['self'])
        # Setup cells
        self.mk_population(GranuleCell, 2000)
        self.mk_population(MossyCell, 60)
        self.mk_population(BasketCell, 24)
        self.mk_population(HippCell, 24)

        # Set seed for reproducibility
        if seed:
            self.set_numpy_seed(seed)

        # Setup recordings
        self.populations[0].record_aps()
        self.populations[1].record_aps()
        self.populations[2].record_aps()
        self.populations[3].record_aps()

        temporal_patterns = np.array(temporal_patterns)
        print(np.shape(temporal_patterns))
        #temporal_patterns = np.atleast_2d(temporal_patterns)
        if type(spatial_patterns_gcs) == np.ndarray and type(temporal_patterns) == np.ndarray:
            #spatial_patterns_gcs = np.atleast_2d(spatial_patterns_gcs)
            for pat in range(len(spatial_patterns_gcs)):
                # PP -> GC
                #Original
                ouropy.gennetwork.PerforantPathPoissonTmgsyn(self.populations[0],
                                                           temporal_patterns[pat],
                                                           spatial_patterns_gcs[pat],
                                                           'midd', 10, 0, 1, 0, 0, 1*10**(-3))

        if type(spatial_patterns_bcs) == np.ndarray and type(temporal_patterns) == np.ndarray:
            #spatial_patterns_bcs = np.atleast_2d(spatial_patterns_bcs)
            for pat in range(len(spatial_patterns_bcs)):
                # PP -> BC
                ouropy.gennetwork.PerforantPathPoissonTmgsyn(self.populations[2],
                                                           temporal_patterns[pat],
                                                           spatial_patterns_bcs[pat],
                                                           'ddend', 6.3, 0, 1, 0, 0, 1*10**(-3))

        # GC -> MC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[0], self.populations[1],
                                  6, 'proxd',
                                  1, 7.6, 500, 0.1, 0, 0, 10, 1.5, 0.2*10**(-2) * 10)

        # GC -> BC
        #Weight x4, target_pool = 2
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[0], self.populations[2],
                                           4, 'proxd',
                                           1, 8.7, 500, 0.1, 0, 0, 10, 0.8, 2.5*10**(-2))

        # GC -> HC
        # Divergence x4; Weight doubled; Connected randomly.
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[0], self.populations[3],
                                           24, 'proxd',
                                           1, 8.7, 500, 0.1, 0, 0, 10, 1.5, 2.5*10**(-2))

        # MC -> MC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[1], self. populations[1],
                                           24, 'proxd',
                                           3, 2.2, 0, 1, 0, 0, 10, 2, 0.5*10**(-3))

        # MC -> BC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[1], self.populations[2],
                                           6, 'proxd',
                                           1, 2, 0, 1, 0, 0, 10, 3, 0.3*10**(-3))

        # MC -> HC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[1], self.populations[3],
                                           10, 'midd',
                                           2, 6.2, 0, 1, 0, 0, 10, 3, 0.2*10**(-3))

        # BC -> GC
        # Nr. synapses x3; Weight *1/4; changed from 5.5 to 20 (Hefft & Jonas, 2005)
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[2], self.populations[0],
                                           280, 'soma',
                                           400, 20, 0, 1, 0, -70, 10, 0.85, 1.2*10**(-3))

        # We reseed here to make sure that those connections are consistent
        # between this and net_global. The only connection that differs between
        # net_tuned and net_global will be the BC -> GC connection.
        if seed:
            self.set_numpy_seed(seed+1)

        # BC -> MC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[2], self.populations[1],
                                           14, 'proxd',
                                           3, 3.3, 0, 1, 0, -70, 10, 1.5, 1.5*10**(-3))

        # BC -> BC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[2], self.populations[2],
                                           6,'proxd',
                                           2, 1.8, 0,1,0,-70, 10, 0.8, 7.6*10**(-3))

        # HC -> GC
        # Weight x10; Nr synapses x4; changed from 6 to 20 (Hefft & Jonas, 2005)
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[3], self.populations[0],
                                           2000, 'dd',
                                           640, 20, 0, 1, 0, -70, 10, 3.8, 0.6*10**(-2))

        # HC -> MC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[3], self.populations[1],
                                           30, ['mid1d', 'mid2d'],
                                           4, 6, 0, 1, 0, -70, 10, 1, 1.5*10**(-3))

        # HC -> BC
        ouropy.gennetwork.tmgsynConnectionExponentialProb(self.populations[3], self.populations[2],
                                           12, 'ddend',
                                           4, 5.8, 0, 1, 0, -70, 10, 1.6, 0.5*10**(-3))
