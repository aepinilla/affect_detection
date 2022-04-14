"""
This script uses data that was recorded and preprocessed by the author of this script,
using a method that is suitable for online analysis.

This script extracts frontal asymmetry and parietal power in the alpha and theta bands.
"""


import pandas as pd

from .settings import d, fs, welch_window_size, bands, exp_videos, electrode_sites, exp_participant_codes, moving_window_size
from .helper import relative_psd_ts, moving_window
from .self_reports import self_reports


def extract_features():
    # Read demgoraphics data file
    demographics = pd.read_csv(d + '/data/subjective/demographics.csv')
    non_outliers = demographics[demographics['Participant Code'].isin(exp_participant_codes)]
    genders = non_outliers[['Participant Code', 'What is your gender?']]

    # Process self_reports
    all_self_reports = self_reports()

    for p in exp_participant_codes:
        # Read participant data
        print("Reading participant %s..." % (p))
        # What is the gender?
        gender = genders.loc[genders['Participant Code'] == p]
        g = gender.iloc[0,1]
        # EEG file name
        file = (d + '/data/objective/preprocessed/eeg/%s_eeg.csv' % (p))
        # Read EEG preprocessed data
        eeg_data = pd.read_csv(file)
        # Subset participant's self-reports
        participant_self_reports = all_self_reports.loc[all_self_reports['participant'] == p]
        # # Find trials
        # trials = participant_self_reports[['video_id', 'trial']]
        # Find start indices
        start = eeg_data['Time'] == 0
        start_idx = start[start]
        # The length of the data of each video is 60 seconds times the sampling frequency (fs), minus 1 sample.
        # The last sample is erased by Matlab
        len_video = (60 * fs) - 1
        # Run once on each band
        band_collection = []
        for band in bands:
            print('Processing %s band' % (band))
            # Run once on each video
            psd_collection = []
            for v in exp_videos:
                print("processing video %s..." % (v))
                # Video data
                eeg_data_video = eeg_data.iloc[start_idx.index[v]:start_idx.index[v]+len_video,:]
                # Video dict
                video_dict = {channel: eeg_data_video[channel] for channel in electrode_sites}
                # Extract the relative Power Spectral Density (PSD)
                # A comprehension dictionary is used to perform this process on each electrode site
                psd_rolling = {channel: relative_psd_ts(moving_window(video_dict[channel].values, moving_window_size), fs, welch_window_size, band=band) for channel in electrode_sites}
                # Transform resulting dictionary into a pandas dataframe
                psd_rolling_df = pd.DataFrame(psd_rolling)
                # Assign video number
                psd_rolling_df['trial'] = v
                # Numerate time series
                psd_rolling_df['timestamp'] = list(range(len(psd_rolling_df)))
                # Append result to list
                psd_collection.append(psd_rolling_df)
                # Transform list with participant's results into a pandas dataframe
            psd_df = pd.concat(psd_collection)
            # Add band name
            psd_df['band'] = band
            # Append band results to list
            band_collection.append(psd_df)
            # Transform list with bands' results into a pandas dataframe
        bands_df = pd.concat(band_collection)
        # Add participant's number
        bands_df['participant'] = p
        # Add subjective data
        bands_df_subjective = pd.merge(bands_df, participant_self_reports, on=['participant', 'trial'])
        # Extract features
        features_dict = {'participant': bands_df_subjective['participant'],
                         'gender': g,
                         'video_id': bands_df_subjective['video_id'],
                         'timestamp': bands_df_subjective['timestamp'],
                         'band': bands_df_subjective['band'],
                         'frontal_asymmetry': bands_df_subjective['F3'] - bands_df_subjective['F4'],
                         'parietal_mean': (bands_df_subjective['P3'] + bands_df_subjective['P4']) / 2,
                         'negativity_rating': bands_df_subjective['negativity_rating'],
                         'positivity_rating': bands_df_subjective['positivity_rating'],
                         'net_predisposition_rating': bands_df_subjective['net_predisposition_rating'],
                         'negativity_type': bands_df_subjective['negativity_type'],
                         'positivity_type': bands_df_subjective['positivity_type'],
                         'net_predisposition_type': bands_df_subjective['net_predisposition_type']}
        features_df = pd.DataFrame(features_dict)
        # Export features to CSV file
        features_df.to_csv((d + '/features/%s_features.csv' % (p)), index=False)


if __name__ == "__main__":
    extract_features()