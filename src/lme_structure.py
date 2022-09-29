"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import pandas as pd
from functools import reduce

from src.helper import melt_df, self_reports
from src.settings import d, eeg_bands, features_list, trials


def lme_structure(p):
    print('Creating files with LME structure for participant ' + p)
    participant_file = pd.read_pickle(d + '/reports/extracted_features/ml/' + p + '.pickle')
    features = participant_file['objective']

    # Features are organised in three groups according to their data structure.
    # That is, whether they include information related to electrode site and power band.
    # This division is useful for conducting the LME analysis.
    # "Base" trials include information related to electrode site.
    # "Relative Power Spectral Density (RPSD)" trials include information related both to electrode site and power band.
    # "Frontal Asymmetry (FA)" trials information related to power band. Frontal asymmetry was extracted only at the frontal
    # region of the brain (difference between activity F3 and F4 electrode sites at each power band).
    all_base_trials = []
    all_rpsd_trials = []
    all_fa_trials = []

    for t in trials:
        # subset trial data
        trial_features = features[t]
        # Collection of features for each trial
        base_features = []
        rpsd_list = []
        fa_list = []
        for f in features_list:
            if f not in ['relative_power_spectral_density', 'frontal_asymmetry']:
                melted_df = melt_df(trial_features[f], name=f)
                base_features.append(melted_df)
            if f == 'relative_power_spectral_density':
                for band, eeg_range in eeg_bands.items():
                    melted_rpsd_df = melt_df(trial_features[f][band], name=f)
                    melted_rpsd_df['band'] = band
                    rpsd_list.append(melted_rpsd_df)
            if f == 'frontal_asymmetry':
                for band, eeg_range in eeg_bands.items():
                    frontal_asymmetry = pd.DataFrame({'frontal_asymmetry': trial_features[f][band], 'band': band})
                    frontal_asymmetry['ts'] = frontal_asymmetry.index
                    fa_list.append(frontal_asymmetry)

        # Merge features
        base_df = reduce(lambda left, right: pd.merge(left, right, on=['electrode', 'ts']), base_features)
        rpsd_df = pd.concat(rpsd_list, axis=0)
        fa_df = pd.concat(fa_list, axis=0)

        # Assign trial number
        base_df['trial'] = t
        rpsd_df['trial'] = t
        fa_df['trial'] = t

        # Append trials
        all_base_trials.append(base_df)
        all_rpsd_trials.append(rpsd_df)
        all_fa_trials.append(fa_df)

    features_groups = {
        'base': pd.concat(all_base_trials),
        'rpsd': pd.concat(all_rpsd_trials),
        'fa': pd.concat(all_fa_trials)
    }

    all_self_reports = self_reports()
    participant_self_reports = all_self_reports.loc[all_self_reports['participant'] == p]

    # Add subjective responses
    for fg in features_groups:
        features_groups[fg] = features_groups[fg].merge(participant_self_reports, on=['trial'])

    # Write data to CSV format for analysis in R
    for fg in features_groups.keys():
        df = features_groups[fg]
        save_path = '/reports/extracted_features/lme/%s/%s.csv' % (fg, p)
        df.to_csv(d + save_path, index=False)


if __name__ == "__main__":
    lme_structure()