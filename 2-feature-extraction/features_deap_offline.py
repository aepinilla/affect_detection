"""
This script uses data that was recorded and preprocessed by the authors of the
DEAP dataset (https://www.eecs.qmul.ac.uk/mmv/datasets/deap/), using a method that is suitable for offline analysis.

This script extracts frontal asymmetry and parietal power in the alpha and theta bands.
"""

import os, sys
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle
from settings import channels_idx, labels_idx, fs, welch_window_size, bands, deap_videos_offline, deap_participants, electrode_sites, moving_window_size
from helper import relative_psd_ts, add_deap_subjective_measures, moving_window

# Define working directory
sys.path.append('../')
d = os.path.dirname(os.getcwd())

def features_deap_offline():
    # Run once on each participant
    for p in deap_participants:
        # Read participant data
        print("Reading participant %s..." % (p))
        x = pickle.load(open(d + '/data/deap/objective_measures_preprocessed_offline/s%s.dat' % (p), 'rb'), encoding='iso-8859-1')
        data = x['data']
        # Run once on each power band (alpha and theta)
        band_collection = []
        for band in bands:
            print('Processing %s band' % (band))
            # Run once on each video
            psd_collection = []
            for v in deap_videos_offline:
                # Read video data
                print("Processing video %s..." % (v))
                # Use EEG data from the electrode sites of interest.
                # The preprocessed data was stored in a three-dimensional array.
                # The first dimension of the array is the number of the video.
                # The second dimension is the channel index.
                # The third dimension is the time series index.
                eeg_data = {'F3': data[v, channels_idx['F3'], :],
                            'F4': data[v, channels_idx['F4'], :],
                            'P3': data[v, channels_idx['P3'], :],
                            'P4': data[v, channels_idx['P4'], :]}
                # Extract the relative Power Spectral Density (PSD) of the current band using the Welch's method.
                # The process is conducted using an 8s Window for the Welch's method. This method is executed several times, using a 10s moving window.
                psd_rolling = {channel: relative_psd_ts(moving_window(eeg_data[channel], moving_window_size), fs, welch_window_size, band=band) for channel in electrode_sites}
                # Transform resulting dictionary into a pandas dataframe
                psd_rolling_df = pd.DataFrame(psd_rolling)
                # Assign video number
                psd_rolling_df['video_id'] = v
                # Numerate time series
                psd_rolling_df['time_stamp'] = list(range(len(psd_rolling_df)))
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
        # Add subjective measures
        bands_df_subjective = add_deap_subjective_measures(bands_df, preprocessing_pipeline='offline')
        # Extract features
        features_dict = {'participant': bands_df_subjective['participant'],
                         'video_id': bands_df_subjective['video_id'],
                         'time_stamp': bands_df_subjective['time_stamp'],
                         'band': bands_df_subjective['band'],
                         'frontal_asymmetry': bands_df_subjective['F3'] - bands_df_subjective['F4'],
                         'parietal_mean': (bands_df_subjective['P3'] + bands_df_subjective['P4']) / 2,
                         'valence_rating': bands_df_subjective['valence_rating'],
                         'arousal_rating': bands_df_subjective['arousal_rating'],
                         'valence_type': bands_df_subjective['valence_type'],
                         'arousal_type': bands_df_subjective['arousal_type']}
        features_df = pd.DataFrame(features_dict)
        # Export features to CSV file
        features_df.to_csv((d + '/features/deap_offline/s%s_features.csv' % (p)), index=False)


if __name__ == "__main__":
    features_deap_offline()