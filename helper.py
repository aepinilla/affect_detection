import os, sys
from os import listdir

import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from scipy import signal
from scipy.integrate import simps
from settings import exp_participant_codes, exp_video_ids_dict
import itertools

# Define working directory
sys.path.append('../')
d = os.path.dirname(os.getcwd())

# Define EEG bands
eeg_bands = {'delta': (0, 4),
             'theta': (4, 8),
             'alpha': (8, 13),
             'beta': (13, 30),
             'gamma': (30, 45)}

def column (matrix, i):
    return np.array(matrix)[:, i]


# Moving window function
def moving_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def relative_psd_ts(x, fs, window, band):
    if band == 'delta':
        low, high = eeg_bands['delta'][0], eeg_bands['delta'][1]
    elif band == 'theta':
        low, high = eeg_bands['theta'][0], eeg_bands['theta'][1]
    elif band == 'alpha':
        low, high = eeg_bands['alpha'][0], eeg_bands['alpha'][1]
    elif band == 'beta':
        low, high = eeg_bands['beta'][0], eeg_bands['beta'][1]
    elif band == 'gamma':
        low, high = eeg_bands['gamma'][0], eeg_bands['gamma'][1]

    # Compute PSD using Welch's method
    freqs, psd = signal.welch(x, fs, nperseg=window)
    # Find frequencies that intersect with alpha band
    idx_band = np.logical_and(freqs >= low, freqs <= high)
    # Calculate frequency resolution
    freq_res = freqs[1] - freqs[0]
    # Compute absolute band power
    band_psd_collection = []
    for i in psd:
        band_power = simps(i[idx_band], dx=freq_res)
        band_psd_collection.append(band_power)
    band_psd = np.asarray(band_psd_collection)
    # Compute total power
    total_power_collection = []
    for i in psd:
        total_power = simps(i, dx=freq_res)
        total_power_collection.append(total_power)
    total_psd = np.asarray(total_power_collection)
    # # Calculate relative alpha power
    relative_band_psd_ts = 100 * (band_psd / total_psd)
    # Take the average PSD of each second
    # scale_factor = 95
    # mean_per_second = [sum(relative_band_psd_ts[i:i + scale_factor]) / scale_factor for i in range(0, len(relative_band_psd_ts), scale_factor)]

    return relative_band_psd_ts


def mahalanobis(x=None, data=None, cov=None):

    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()


def find_csv_filenames(path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
