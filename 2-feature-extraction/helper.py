import os, sys
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from scipy import signal
from scipy.integrate import simps


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