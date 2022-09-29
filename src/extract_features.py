"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

"""
Extracts features using a mobile window.
The following features are extracted at each electrode site:
- Spectral envelope
- Zero crossings
- Katz fractal_dimension
- Hjorth activity
- Hjorth movility
- Hjorth complexity
- Petrosian fractal dimension

The following feature is extracted at each power band AND at each electrode site:
- Relative power spectral density

The following feature is extracted at each power band:
- Frontal asymmetry
"""

from antropy import hjorth_params, katz_fd, num_zerocross, petrosian_fd, spectral_entropy
from numpy.lib.stride_tricks import sliding_window_view
import pandas as pd
import pickle

from src.helper import hp_activity_ts, relative_psd_ts, self_reports, start_idx
from src.settings import d, eeg_bands, len_epoch, sliding_window_size, trials, fs, welch_window_size


def extract_features(p):
    print("Reading participant %s..." % (p))
    preprocessed_file_name = (d + '/data/objective/preprocessed/eeg/%s_eeg.csv' % (p))
    eeg_data = pd.read_csv(preprocessed_file_name)
    electrode_sites = eeg_data.columns[1:].values.tolist()
    epochs_start_mark = start_idx(eeg_data)
    all_trials = {}
    # Extract features for each video trial
    for t in trials:
        print("processing video %s..." % (t))
        eeg_data_video = eeg_data.iloc[epochs_start_mark.index[t]:epochs_start_mark.index[t]+len_epoch,:]
        eeg_data_video_dict = {channel: eeg_data_video[channel] for channel in electrode_sites}
        # Spectral envelope
        se = {channel: spectral_entropy(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size), fs, method='welch', nperseg=welch_window_size, normalize=True) for channel in electrode_sites}
        # Number of zero-crossings
        zc = {channel: num_zerocross(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size)) for channel in electrode_sites}
        # Katz fractal dimension
        kfd = {channel: katz_fd(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size)) for channel in electrode_sites}
        # Hjorth parameters
        # Hjorth Activity
        ha = {channel: hp_activity_ts(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size)) for channel in electrode_sites}
        # Hjorth Movement and Mobility
        hmc = {channel: hjorth_params(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size)) for channel in electrode_sites}
        # Split mobility and complexity to separate dictionaries
        hm = {channel: hmc[channel][0] for channel in electrode_sites}
        hc = {channel: hmc[channel][1] for channel in electrode_sites}
        # Petrosian Fractal Dimension
        pfd = {channel: petrosian_fd(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size)) for channel in electrode_sites}
        # Extract Relative Power Spectral Density and Frontal Asymmetry on each power band
        rpsd_bands = {}
        fa_bands = {}
        for band, eeg_range in eeg_bands.items():
            print('Processing %s band' % (band))
            # Relative Power Spectral Density
            rpsd = {channel: relative_psd_ts(sliding_window_view(eeg_data_video_dict[channel], sliding_window_size), fs, welch_window_size, eeg_range) for channel in electrode_sites}
            rpsd_bands[band] = rpsd
            # Frontal asymmetry
            fa = rpsd['F3'] - rpsd['F4']
            fa_bands[band] = fa

        features_dict = {
            'spectral_envelope': se,
            'zero_crossings': zc,
            'katz_fractal_dimension': kfd,
            'hjorth_activity': ha,
            'hjorth_movility': hm,
            'hjorth_complexity': hc,
            'petrosian_fractal_dimension': pfd,
            'relative_power_spectral_density': rpsd_bands,
            'frontal_asymmetry': fa_bands
        }

        all_trials[t] = features_dict

    all_self_reports = self_reports()
    participant_self_reports = all_self_reports.loc[all_self_reports['participant'] == p]

    participant_data = {
        'objective': all_trials,
        'subjective': participant_self_reports
    }

    features_file_name = d + '/reports/extracted_features/ml/' + p + '.pickle'
    with open(features_file_name, 'wb') as handle:
        pickle.dump(participant_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    extract_features()