"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import pandas as pd
from collections import defaultdict

from src.helper import get_lme_results, subset_trials_ml
from src.settings import d, dimensions, trials


def select_features_lme(p, rs):
    # Load data
    participant_data = pd.read_pickle(d + "/reports/extracted_features/ml/%s.pickle" % (p))
    participant_features = participant_data['objective']
    lme_results = get_lme_results(p)
    lme_results_iteration = lme_results.loc[lme_results['iteration'] == rs]
    # Which features are relevant for the selected participant?
    # Build dict with names of selected features, as per LME analysis
    features_names_dimensions = {}
    for dim in dimensions:
        dimension_mask = lme_results_iteration['dimension'].str.contains(dim)
        dimension_features = lme_results_iteration.loc[dimension_mask]
        features_names = dimension_features['feature'].unique()
        features_names_dimensions[dim] = features_names

    # Filter out non-relevant features, as per the LME analysis
    nested_dict = lambda: defaultdict(nested_dict)
    selected_features = nested_dict()
    for dim in dimensions:
        relevant_features_dim = features_names_dimensions[dim]
        for t in trials:
            for f in relevant_features_dim:
                if f not in ['relative_power_spectral_density', 'frontal_asymmetry']:
                    this_feature = dimension_features.loc[dimension_features['feature'] == f]
                    relevant_electrodes = this_feature['electrode'].unique()
                    for e in relevant_electrodes:
                        selected_features[dim][t][f][e] = participant_features[t][f][e]
                if f == 'relative_power_spectral_density':
                    this_feature = dimension_features.loc[dimension_features['feature'] == f]
                    relevant_bands = this_feature['band'].unique()
                    for b in relevant_bands:
                        this_band = this_feature.loc[this_feature['band'] == b]
                        relevant_electrodes = this_band['electrode'].unique()
                        for e in relevant_electrodes:
                            selected_features[dim][t][f][b][e] = participant_features[t][f][b][e]
                if f == 'frontal_asymmetry':
                    this_feature = dimension_features.loc[dimension_features['feature'] == f]
                    relevant_bands = this_feature['band'].unique()
                    for b in relevant_bands:
                        selected_features[dim][t][f][b] = participant_features[t][f][b]
                else:
                    continue

    # Select trials that were not used in the LME analysis. This is necessary to prevent double-dipping.
    participant_ml_data = subset_trials_ml(p, selected_features, rs)
    return participant_ml_data


if __name__ == "__main__":
    select_features_lme()