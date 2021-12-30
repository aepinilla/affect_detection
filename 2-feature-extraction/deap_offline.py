"""
Extracts the relative Power Spectral Density (PSD) at the Alpha and Theta bands using the Welch's method.
This process is conducted in 4 electrode sites: F3, F4, P3 and P4.
Then, Frontal Asymmetry and Parietal Power are calculated.
"""

import os, sys
import pandas as pd
import pickle
from settings import channels_idx, fs, welch_window_size, bands, deap_videos, deap_participants, electrode_sites
from helper import relative_psd

# Define working directory
sys.path.append('../')
d = os.path.dirname(os.getcwd())

def extract_features_deap_offline():
    # Run once on each power band (alpha and theta)
    band_collection = []
    for band in bands:
        print('Processing %s band' % (band))
        # Run once on each participant
        participants_collection = []
        for p in deap_participants:
            # Read participant data
            print("reading participant %s..." % (p))
            x = pickle.load(open(d + '/data/deap_offline/objective/s%s.dat' % (p), 'rb'), encoding='iso-8859-1')
            data = x['data']
            # Run once on each video
            band_psd_collection = []
            for v in deap_videos:
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
                # Append result to list
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

    # Extract features
    features = pd.DataFrame()
    features['participant'] = power['participant']
    features['video_id'] = power['video_id']
    features['band'] = power['band']
    features['frontal_asymmetry'] = power['F3'] - power['F4']
    features['parietal_mean'] = (power['P3'] + power['P4']) / 2

    # Export features to CSV file
    features.to_csv((d + '/data/deap_offline/deap_offline_features.csv'), index=False)


if __name__ == "__main__":
    extract_features_deap_offline()