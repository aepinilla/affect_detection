import os, sys
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from scipy import signal
from scipy.integrate import simps
from settings import exp_participant_codes, exp_video_ids_dict


# Define working directory
sys.path.append('../')
d = os.path.dirname(os.getcwd())

# Define EEG bands
eeg_bands = {'delta': (0, 4),
             'theta': (4, 8),
             'alpha': (8, 13),
             'beta': (13, 30),
             'gamma': (30, 45)}

def relative_psd(x, fs, window, band):
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
    # Find frequencies that intersect with selected band
    idx_band = np.logical_and(freqs >= low, freqs <= high)
    # Calculate frequency resolution
    freq_res = freqs[1] - freqs[0]
    # Compute absolute band power
    band_power = simps(psd[idx_band], dx=freq_res)
    # Compute total power
    total_power = simps(psd, dx=freq_res)
    # # Calculate relative band power
    relative_band = 100 * (band_power / total_power)

    return relative_band


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

    return relative_band_psd_ts


def add_deap_subjective_measures(power, preprocessing_pipeline):
    # Read Excel file with video types
    vl = pd.read_excel(d + '/data/deap/subjective_measures/video_list.xls')
    # Define quadrants
    quadrants = vl[['Experiment_id', 'VAQ_Online']]
    quadrants.columns = ['video_id', 'quadrant']
    # Arousal video types
    quadrants.loc[quadrants['quadrant'] == 1, 'arousal_type'] = 'HA'
    quadrants.loc[quadrants['quadrant'] == 2, 'arousal_type'] = 'LA'
    quadrants.loc[quadrants['quadrant'] == 3, 'arousal_type'] = 'LA'
    quadrants.loc[quadrants['quadrant'] == 4, 'arousal_type'] = 'HA'
    # Valence video types
    quadrants.loc[quadrants['quadrant'] == 1, 'valence_type'] = 'HV'
    quadrants.loc[quadrants['quadrant'] == 2, 'valence_type'] = 'HV'
    quadrants.loc[quadrants['quadrant'] == 3, 'valence_type'] = 'LV'
    quadrants.loc[quadrants['quadrant'] == 4, 'valence_type'] = 'LV'
    # Drop empty rows
    quadrants = quadrants.dropna()
    # Read subjective ratings
    ratings = pd.read_excel(d + '/data/deap/subjective_measures/participant_ratings.xls')
    ratings = ratings[['Participant_id', 'Experiment_id', 'Valence', 'Arousal']]
    ratings.columns = ['participant', 'video_id', 'valence_rating', 'arousal_rating']
    # Add quadrants
    ratings_quadrants = pd.merge(ratings, quadrants, on=['video_id'])
    # In the data that was preprocessed by the authors of the DEAP dataset increase all values of video id by 1.
    # This is necessary because in the .dat files videos are 0-indexed, while the Excel file with the quadrant types, videos are 1-indexed
    if preprocessing_pipeline == 'offline':
        power['video_id'] = power['video_id'] + 1
    # Add quadrants
    power_ratings_quadrants = power.merge(ratings_quadrants, on=['participant', 'video_id'])

    return power_ratings_quadrants

# Self-reports
def add_exp_subjective_measures(power):
    self_reports_collection = []
    for p in exp_participant_codes:
        # Read data
        filename = d + '/data/pilot_exp/subjective/self_reports/%s_self_report.csv' % (p)
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
    all_self_reports = all_self_reports[
        ['participant', 'video_id', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]
    # Add quadrants
    quadrants = all_self_reports.loc[:,
                ['video_id', 'participant', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]
    # quadrants = quadrants.groupby(['video_id']).mean().reset_index()
    quadrants.loc[quadrants['negativity_rating'] < 5, 'negativity_type'] = 'LN'
    quadrants.loc[quadrants['negativity_rating'] > 5, 'negativity_type'] = 'HN'
    quadrants.loc[quadrants['positivity_rating'] < 5, 'positivity_type'] = 'LP'
    quadrants.loc[quadrants['positivity_rating'] > 5, 'positivity_type'] = 'HP'
    quadrants.loc[quadrants['net_predisposition_rating'] < 5, 'net_predisposition_type'] = 'LNP'
    quadrants.loc[quadrants['net_predisposition_rating'] > 5, 'net_predisposition_type'] = 'HNP'
    quadrants = quadrants.drop(columns=['negativity_rating', 'positivity_rating', 'net_predisposition_rating'])
    # Add quadrants to subjective ratings
    subjective_quadrants = pd.merge(all_self_reports, quadrants, on=['participant', 'video_id'])
    # Merge self-reports with PSD data
    power_subjective = power.merge(subjective_quadrants, on=['participant', 'video_id'])

    return power_subjective

# create function to calculate Mahalanobis distance
def mahalanobis(x=None, data=None, cov=None):

    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()