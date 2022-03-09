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


def add_exp_subjective_measures(power):
    self_reports_collection = []
    for p in exp_participant_codes:
        # Read data
        filename = d + '/affect_detection/data/subjective/self_reports/%s_self_report.csv' % (p)
        psychopy_data = pd.read_csv(filename)
        self_reports = psychopy_data[
            ['videoFile', 'likertNegativity.response', 'likertPositivity.response', 'likertArousal.response']]
        self_reports = self_reports.dropna().reset_index(drop=True)
        # Add participant code
        self_reports['participant_code'] = p
        # Create empty column for video codes
        self_reports['video_id'] = 'NaN'
        # Assign video codes
        for key, value in exp_video_ids_dict.items():
            self_reports.loc[self_reports['videoFile'] == key, 'video_id'] = value
        # Rename columns
        self_reports.columns = ['video_file', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating',
                                'participant', 'video_id']
        # Add self-report to list
        self_reports_collection.append(self_reports)
    # Concatenate all self-reports
    all_self_reports = pd.concat(self_reports_collection)
    all_self_reports = all_self_reports[['participant', 'video_id', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]
    # Merge self-reports with PSD data
    power_subjective = power.merge(all_self_reports, on=['participant', 'video_id'])

    return power_subjective


def mahalanobis(x=None, data=None, cov=None):

    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()


def get_exp_self_reports():
    self_reports_collection = []
    for p in exp_participant_codes:
        # Read data
        filename = d + '/affect_detection/data/subjective/self_reports/%s_self_report.csv' % (p)
        psychopy_data = pd.read_csv(filename)
        self_reports = psychopy_data[['videoFile', 'likertNegativity.response', 'likertPositivity.response', 'likertArousal.response']]
        self_reports = self_reports.dropna().reset_index(drop=True)

        # Add participant code
        self_reports['participant_code'] = p

        # Create empty column for video codes
        self_reports['video_id'] = 'NaN'

        # Add video number (trial number)
        self_reports['trial'] = list(range(1, 17))

        # Assign video codes
        for key, value in exp_video_ids_dict.items():
            self_reports.loc[self_reports['videoFile'] == key, 'video_id'] = value

        # Rename columns
        self_reports.columns = ['video_file', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating', 'participant', 'video_id', 'trial']

        # Add self-report to list
        self_reports_collection.append(self_reports)

    all_self_reports = pd.concat(self_reports_collection)
    all_self_reports = all_self_reports[['participant', 'video_id', 'trial', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]

    return all_self_reports


def find_csv_filenames(path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
