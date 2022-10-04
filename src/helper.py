"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from collections import defaultdict
from flatten_dict import flatten
from itertools import compress
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
from os import listdir
from os.path import isfile, join
from scipy import signal
from scipy.integrate import simps

from src.settings import d, dimensions, feature_groups, fs_dataset_ratio, participants_codes, trials, video_ids


def conduct_iqr(data):
    # Perform IQR
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    # The code below removes responses that lie more than 1.5 times the IQR, above the 3rd quantile or below the 1st quantile.
    outliers = data[((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
    participants_outliers = outliers.participant.unique()
    return participants_outliers


def extract_bands(lst):
    return [item[0] for item in lst]


def extract_selected_features_names(dimension_results):
    features_set = []
    all_features = []
    for dr in list(range(0, len(dimension_results))):
        this_feature = dimension_results[dr].split(".")
        features_set.append(this_feature[0])
        all_features.append(this_feature)

    features_set = set(features_set)
    features_set_dict = dict.fromkeys(features_set, [])
    all_features_len = list(range(0, len(all_features)))

    for f in features_set:
        details_feature = []
        for i in all_features_len:
            if f in all_features[i]:
                details_feature.append(all_features[i][1:])
                features_set_dict[f] = details_feature

    features_set_dict_indent = indent_bands(features_set_dict)
    return features_set_dict_indent


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def get_lme_results(p):
    # Which features are relevant for the selected participant?
    relevant_features = {}
    # Read results from LME models
    for fg in feature_groups:
        dir_path = d + "/reports/feature_selection/lme/%s/" % (fg)
        # Build list with all files
        files_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        # Subset files of current participant
        participant_files_list = [s for s in files_list if p in s]
        # Read all results of current participant
        participant_dfs_list = []
        for file in participant_files_list:
            # Ignore Mac system file
            if file != ".DS_Store":
                df = pd.read_feather(dir_path + file)
                participant_dfs_list.append(df)

        # Concatenate all files
        participant_feature_group = pd.concat(participant_dfs_list)
        # Subset features where a significant effect was found with the likelihood ratio test
        significant_effects_feature_group = participant_feature_group.loc[participant_feature_group["Pr(>Chisq)"] < 0.05]
        relevant_features[fg] = significant_effects_feature_group

    # Concatenate all relevant features
    base_feature_group = relevant_features['base'][['dimension', 'feature', 'electrode', 'iteration']]
    rpsd_feature_group = relevant_features['rpsd'][['dimension', 'feature', 'electrode', 'band', 'iteration']]
    fa_feature_group = relevant_features['fa'][['dimension', 'feature', 'band', 'iteration']]
    all_relevant_features = pd.concat([base_feature_group, rpsd_feature_group, fa_feature_group])

    return all_relevant_features


def get_rfecv_data(i, participant_features, p):
    print('RFECV iteration ' + str(i))
    # Which trials will be used for Recursive Feature Elimination?
    # These trials should be different from the trials that will be used for training the model
    # Initialize nested dictionary
    nested_dict = lambda: defaultdict(nested_dict)
    # Load self reports
    all_self_reports = self_reports()
    participant_self_reports = all_self_reports.loc[all_self_reports["participant"] == p]
    # Get indices for randomly splitting data
    random_indices = pd.read_csv(d + '/reports/random_indices/' + p + '.csv')
    trial_indices = random_indices.loc[random_indices.iteration == i]
    trials_dict = {}
    for dim in dimensions:
        mask = np.isin(trials, trial_indices[dim])
        dimension_trials = list(compress(trials, mask))
        trials_dict[dim] = dimension_trials
    # Subset trials
    relevant_trials = {}
    for dim in dimensions:
        relevant_data_for_ml = {key: value for (key, value) in participant_features.items() if key in trials_dict[dim]}
        relevant_trials[dim] = relevant_data_for_ml

    # Adjust data structure for RFECV
    rfecv_data = nested_dict()
    for dim in dimensions:
        # Flatten dictionaries
        trials_flattened = []
        for mt in trials_dict[dim]:
            flatten_trial = flatten(relevant_trials[dim][mt])
            trial_df = pd.DataFrame.from_dict(flatten_trial)
            trial_df['trial'] = mt
            trials_flattened.append(trial_df)
        trials_df = pd.concat(trials_flattened)

        # Remove multilevel index
        trials_df.columns = trials_df.columns.to_flat_index()
        number_of_columns = list(range(0, len(trials_df.columns)))
        delimiter = '.'
        for n in number_of_columns:
            column_name_tuple = trials_df.columns[n]
            column_name_string = delimiter.join([str(value) for value in column_name_tuple])
            column_name_no_nan = column_name_string.replace(".nan", "")
            trials_df.columns.values[n] = column_name_no_nan

        # Rename last column as trial to merge with labels dataframe
        trials_df.columns = [*trials_df.columns[:-1], 'trial']
        # Add labels
        relevant_trial_subjective_data = participant_self_reports[
            participant_self_reports['trial'].isin(relevant_trials[dim])]
        relevant_trial_subjective_data = relevant_trial_subjective_data[['trial', ('%s_type' % (dim))]]
        dimension_relevant_features_with_labels = pd.merge(trials_df, relevant_trial_subjective_data, on='trial')
        dimension_relevant_features_with_labels = dimension_relevant_features_with_labels.drop(['trial'],
                                                                                               axis=1)
        # Split features and labels
        selected_features = dimension_relevant_features_with_labels[dimension_relevant_features_with_labels.columns[:-1]]
        corresponding_labels = dimension_relevant_features_with_labels[[('%s_type' % (dim))]]
        rfecv_data[dim]['features'] = selected_features
        rfecv_data[dim]['labels'] = corresponding_labels

    return rfecv_data


def get_split_indices(participant_self_reports, random_state):
    n_trials_fs_set = round((len(participant_self_reports) * fs_dataset_ratio))

    split_data_indices = {}
    for dim in dimensions:
        all_high_idx = pd.Series(participant_self_reports.loc[participant_self_reports[dim + '_type'] == 1].trial.values)
        all_low_idx = pd.Series(participant_self_reports.loc[participant_self_reports[dim + '_type'] == 0].trial.values)

        subset_high_idx = all_high_idx.sample(n=(n_trials_fs_set//2), random_state=random_state).values
        subset_low_idx = all_low_idx.sample(n=(n_trials_fs_set//2), random_state=random_state).values

        split_data_indices[dim] = np.concatenate([subset_high_idx, subset_low_idx])

    return split_data_indices


def hp_activity_ts(x):
    activity_collection = []
    for s in x:
        activity = np.var(s)
        nonan_activity = np.nanmean(activity)
        activity_collection.append(nonan_activity)

    hp_activity = np.array(activity_collection)

    return hp_activity


def indent_bands(features_set_dict):
    try:
        f = 'relative_power_spectral_density'
        bands_list = extract_bands(features_set_dict[f])
        bands_dict = dict.fromkeys(bands_list, [])
        for b, e in bands_dict.items():
            electrodes_band = []
            for fsd in features_set_dict[f]:
                if b in fsd:
                    electrodes_band.append(fsd[1:])
            bands_dict[b] = electrodes_band

        features_set_dict[f] = bands_dict
    except:
        pass
    return features_set_dict


def melt_df(dict, name=''):
    df = pd.DataFrame.from_dict(dict, orient='columns')
    df['ts'] = df.index
    df_melt = pd.melt(df, id_vars='ts', var_name='electrode', value_name=name)
    return df_melt


def relative_psd_ts(x, fs, window, eeg_range):
    # Frequency ranges
    low = eeg_range[0]
    high = eeg_range[1]
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


def self_reports():
    self_reports_collection = []
    for p in participants_codes:
        # Read data
        filename = d + '/data/subjective/self_reports/%s_self_report.csv' % (p)
        psychopy_data = pd.read_csv(filename)
        self_report = psychopy_data[['videoFile', 'likertNegativity.response', 'likertPositivity.response', 'likertArousal.response']]
        self_report = self_report.dropna().reset_index(drop=True)

        # Add participant code
        self_report['participant_code'] = p
        # Create empty column for video codes
        self_report['video_id'] = 'NaN'
        # Add video number (trial number)
        self_report['trial'] = list(range(1, 17))

        # Assign video codes
        for key, value in video_ids.items():
            self_report.loc[self_report['videoFile'] == key, 'video_id'] = value

        # Rename columns
        self_report.columns = ['video_file', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating', 'participant', 'video_id', 'trial']
        # Add self-report to list
        self_reports_collection.append(self_report)

    all_self_reports = pd.concat(self_reports_collection)
    all_self_reports = all_self_reports[['participant', 'video_id', 'trial', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]

    # Define video types for negativity
    all_self_reports.loc[all_self_reports['negativity_rating'] >= 5, 'negativity_type'] = 1
    all_self_reports.loc[all_self_reports['negativity_rating'] < 5, 'negativity_type'] = 0

    # Define video types for positivity
    all_self_reports.loc[all_self_reports['positivity_rating'] >= 5, 'positivity_type'] = 1
    all_self_reports.loc[all_self_reports['positivity_rating'] < 5, 'positivity_type'] = 0

    # Define video types for net predisposition
    all_self_reports.loc[all_self_reports['net_predisposition_rating'] >= 5, 'net_predisposition_type'] = 1
    all_self_reports.loc[all_self_reports['net_predisposition_rating'] < 5, 'net_predisposition_type'] = 0

    return all_self_reports


def start_idx(data):
    start = data['Time'] == 0
    start_idx = start[start]
    return start_idx


def subset_trials_ml(p, selected_features, random_state):
    # Which trials will be used for training and testing the classification models?
    # These trials should be different from the trials that were used for the RFECV analysis
    nested_dict = lambda: defaultdict(nested_dict)

    all_self_reports = self_reports()
    participant_self_reports = all_self_reports.loc[all_self_reports["participant"] == p]
    random_trials = get_split_indices(participant_self_reports, random_state)

    ml_trials = {}
    for dim in dimensions:
        mask = ~np.isin(trials, random_trials[dim])
        dimension_trials = list(compress(trials, mask))
        ml_trials[dim] = dimension_trials

    # Subset trials that will be used in the ML models
    relevant_participant_data = {}
    for dim in dimensions:
        relevant_data_for_ml = {key: value for (key, value) in selected_features[dim].items() if key in ml_trials[dim]}
        relevant_participant_data[dim] = relevant_data_for_ml

    training_and_testing_data = nested_dict()
    for dim in dimensions:
        # Flatten dictionaries
        trials_flattened = []
        for mt in ml_trials[dim]:
            flatten_trial = flatten(relevant_participant_data[dim][mt])
            trial_df = pd.DataFrame.from_dict(flatten_trial)
            trial_df['trial'] = mt
            trials_flattened.append(trial_df)
        trials_df = pd.concat(trials_flattened)
        # Remove multilevel index
        trials_df_reset_index = trials_df.T.reset_index(drop=True).T
        # Rename last column as trial to merge with labels dataframe
        trials_df_reset_index.columns = [*trials_df_reset_index.columns[:-1], 'trial']

        # Add labels
        subjective_ml_trials = participant_self_reports[participant_self_reports['trial'].isin(ml_trials[dim])]
        subjective_ml_trials = subjective_ml_trials[['trial', ('%s_type' % (dim))]]
        dimension_relevant_features_with_labels = pd.merge(trials_df_reset_index, subjective_ml_trials, on='trial')
        dimension_relevant_features_with_labels = dimension_relevant_features_with_labels.drop(['trial'], axis=1)

        selected_features = dimension_relevant_features_with_labels.iloc[:, :-1].values
        corresponding_labels = dimension_relevant_features_with_labels.iloc[:, -1].values

        training_and_testing_data[dim]['features'] = selected_features
        training_and_testing_data[dim]['labels'] = corresponding_labels

    return training_and_testing_data