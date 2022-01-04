"""
This script uses data that was recorded by the authors of the DEAP dataset (https://www.eecs.qmul.ac.uk/mmv/datasets/deap/)
The data was preprocessed by the author of this script using a method that is suitable for online analysis.

This script extracts frontal asymmetry and parietal power in the alpha and theta bands.
"""

import os, sys
sys.path.append('../')

import pandas as pd
pd.options.mode.chained_assignment = None
from settings import fs, welch_window_size, bands, deap_videos_online, deap_participants, electrode_sites
from helper import relative_psd, add_deap_subjective_measures

# Define working directory
d = os.path.dirname(os.getcwd())

def features_deap_online():
    # Run once on each power band
    band_collection = []
    for band in bands:
        print('Processing %s band' % (band))
        # Run once on each participant
        participants_collection = []
        for p in deap_participants:
            # Read participant data
            print("reading participant %s..." % (p))
            # File name
            file = (d + '/data/deap/objective_measures_preprocessed_online/preprocessed/s%s.csv' % (p))
            # Read ratings file
            ratings = pd.read_excel(d + '/data/deap/subjective_measures/participant_ratings.xls')
            # Extract data from current participant
            trials = ratings[ratings['Participant_id'] == p]
            # Extract trial numbers and experiment ids key-pairs
            trials = trials[['Trial', 'Experiment_id']]
            # Rename columns
            trials.columns = ['trial', 'video_id']
            # All data
            eeg_data = pd.read_csv(file)

            # Find start indices
            start = eeg_data['Time'] == 0
            start_idx = start[start]

            # Find end indices
            end = eeg_data['Time'] >= 59992
            end_idx = end[end]

            # Run once on each video
            band_psd_collection = []
            for v in deap_videos_online:
                print("processing video %s..." % (v))
                # Video data
                video_data = eeg_data.iloc[start_idx.index[v - 1]:end_idx.index[v - 1],:]
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
            # Write participant number
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
    # Add subjective measures
    power_subjective = add_deap_subjective_measures(power, preprocessing_pipeline='online')
    # Extract features
    features_dict = {'participant': power_subjective['participant'],
                     'video_id': power_subjective['video_id'],
                     'band': power_subjective['band'],
                     'frontal_asymmetry': power_subjective['F3'] - power_subjective['F4'],
                     'parietal_mean': (power_subjective['P3'] + power_subjective['P4']) / 2,
                     'valence_rating': power_subjective['valence_rating'],
                     'arousal_rating': power_subjective['arousal_rating'],
                     'valence_type': power_subjective['valence_type'],
                     'arousal_type': power_subjective['arousal_type']}
    features_df = pd.DataFrame(features_dict)
    # Export power and features to separate CSV files
    features_df.to_csv((d + '/features/deap_online_features.csv'), index=False)


if __name__ == "__main__":
    features_deap_online()