#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Functions to analyses VC traces
"""

from brian2 import *

def find_spikes_at(data, dt, thres):
    # calculate spike timing when AP crossed 0mV\n"
    spikes = np.zeros(len(data))
    above_thres1 = np.where(data[:-1] <=thres)
    spikes[above_thres1] = 1
    spikes_shift = np.zeros(len(data))
    above_thres2 = np.where(data[1:] <=thres)
    spikes_shift[above_thres2] = 1
    spike_times = spikes_shift-spikes
    spike_times = np.where(spike_times == 1)[0]
    spike_times = spike_times*dt # in ms\n"
    return spike_times

def find_peak(data, dt, t_transient):
    start = int(t_transient/dt)
    end = int(t_transient/dt+0.0002/dt)
    peak_idx = np.argmin(data[start:end]) + start
    return peak_idx, data[peak_idx]
