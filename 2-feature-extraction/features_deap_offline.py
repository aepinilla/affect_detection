"""
This script uses data that was recorded and preprocessed by the authors of the
DEAP dataset (https://www.eecs.qmul.ac.uk/mmv/datasets/deap/), using a method that is suitable for offline analysis.

This script extracts frontal asymmetry and parietal power in the alpha and theta bands.
"""

import os, sys
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle
from settings import channels_idx, labels_idx, fs, welch_window_size, bands, deap_videos_offline, deap_participants, electrode_sites
from helper import relative_psd, add_deap_subjective_measures

# Define working directory
sys.path.append('../')
d = os.path.dirname(os.getcwd())

def features_deap_offline():
    # Run once on each power band (alpha and theta)
    band_collection = []
    for band in bands:
        print('Processing %s band' % (band))
        # Run once on each participant
        participants_collection = []
        for p in deap_participants:
            # Read participant data
            print("reading participant %s..." % (p))
            x = pickle.load(open(d + '/data/deap/objective_measures_preprocessed_offline/s%s.dat' % (p), 'rb'), encoding='iso-8859-1')
            data = x['data']
            labels = x['labels']
            # Run once on each video
            band_psd_collection = []
            for v in deap_videos_offline:
                # Read video data
                print("processing video %s..." % (v))
                # Use EEG data from the electrode sites of interest.
                # The preprocessed data was stored in a three-dimensional array.
                # The first dimension of the array is the number of the video.
                # The second dimension is the channel index.
                # The third dimension is the time series index.
                eeg_data = {'F3': data[v, channels_idx['F3'], :],
                            'F4': data[v, channels_idx['F4'], :],
                            'P3': data[v, channels_idx['P3'], :],
                            'P4': data[v, channels_idx['P4'], :]}
                # Extract the relative Power Spectral Density (PSD) on the 4 electrode sites of interest.
                psd = {channel: relative_psd(eeg_data[channel], fs, welch_window_size, band = band) for channel in electrode_sites}
                # Transform resulting dictionary into a pandas dataframe
                psd_df = pd.DataFrame(psd, index=[0])
                # Add video number
                psd_df['video_id'] = v
                # Append PSD to collection
                band_psd_collection.append(psd_df)
            # Transform list with participant's results into a pandas dataframe
            participant_df = pd.concat(band_psd_collection)
            # Add participant's number
            participant_df['participant'] = p
            # Add to participants collection
            participants_collection.append(participant_df)
        # Concatenate all participants
        all_participants = pd.concat(participants_collection)
        # Write band name
        all_participants['band'] = band
        # Add to collection
        band_collection.append(all_participants)
    # Concatenate data from alpha and theta bands
    power = pd.concat(band_collection)
    # Add subjective measures
    power_subjective = add_deap_subjective_measures(power, preprocessing_pipeline='offline')
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
    # Export features to CSV file
    features_df.to_csv((d + '/features/deap_offline_features.csv'), index=False)


if __name__ == "__main__":
    features_deap_offline()