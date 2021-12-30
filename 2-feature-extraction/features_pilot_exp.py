"""
This script uses data that was recorded and preprocessed by the author of this script,
using a method that is suitable for online analysis.

This script extracts frontal asymmetry and parietal power in the alpha and theta bands.
"""

import os, sys
sys.path.append('../')

import pandas as pd
from settings import fs, welch_window_size, bands, exp_videos, electrode_sites, exp_participant_codes
from helper import relative_psd
from get_exp_self_reports import get_exp_self_reports

# Define working directory
d = os.path.dirname(os.getcwd())

def features_pilot_exp():
    # Get all self reports
    all_self_reports = get_exp_self_reports()
    # Run once on each power band
    band_collection = []
    for band in bands:
        print('Processing %s band' % (band))
        # Run once on each participant
        participants_collection = []

        alpha_collection = []
        for p in exp_participant_codes:
            # Read participant data
            print("reading participant %s..." % (p))
            # EEG file name
            file = (d + '/data/pilot_exp/objective/preprocessed/eeg/%s_eeg.csv' % (p))
            # Read EEG preprocessed data
            eeg_data = pd.read_csv(file)
            # Read self-reports
            trials = all_self_reports[all_self_reports['participant'] == p]
            trials = trials[['video_id', 'trial']]
            # Find start indices
            start = eeg_data['Time'] == 0
            start_idx = start[start]
            # Find end indices
            end = eeg_data['Time'] >= 59992
            end_idx = end[end]
            # Run once on each video
            band_psd_collection = []
            for v in exp_videos:
                print("processing video %s..." % (v))
                # Video data
                video_data = eeg_data[start_idx.index[v - 1]:end_idx.index[v - 1]]
                # Video dict
                video_dict = {channel: video_data[channel] for channel in electrode_sites}
                # Extract the relative Power Spectral Density (PSD)
                # A comprehension dictionary is used to perform this process on each electrode site
                psd = {channel: relative_psd(video_dict[channel], fs, welch_window_size, band = band) for channel in electrode_sites}
                # Transform resulting dictionary into a pandas dataframe
                psd_df = pd.DataFrame(psd, index=[0])
                # Write trial number
                psd_df['trial'] = v
                # Append result to list
                band_psd_collection.append(psd_df)
            # Transform list with participant's results into a pandas dataframe
            participant_df = pd.concat(band_psd_collection)
            # Write participant code
            participant_df['participant'] = p
            # Write video ids
            participant_df_ids = pd.merge(participant_df, trials, on='trial')
            # Add to participants collection
            participants_collection.append(participant_df_ids)
        # Concatenate participants
        all_participants = pd.concat(participants_collection)
        # Write band name
        all_participants['band'] = band
        # Add to band collection
        band_collection.append(all_participants)
    # Concatenate bands
    power = pd.concat(band_collection)

    # Extract features
    features = pd.DataFrame()
    features['participant'] = power['participant']
    features['video_id'] = power['video_id']
    features['band'] = power['band']
    features['frontal_asymmetry'] = power['F3'] - power['F4']
    features['parietal_mean'] = (power['P3'] + power['P4']) / 2

    # Export power and features to separate CSV files
    features.to_csv((d + '/features/pilot_exp_features.csv'), index=False)


if __name__ == "__main__":
    features_pilot_exp()