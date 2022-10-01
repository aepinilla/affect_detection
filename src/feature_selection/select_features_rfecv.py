"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import pandas as pd
from collections import defaultdict

from src.helper import extract_selected_features_names, flatten_list, subset_trials_ml
from src.settings import d, dimensions, trials


"""
Takes two arguments:
p: the participant code.
rs: the random state value used for obtaining replicable results with randomisation.
"""
def select_features_rfecv(p, rs):
    # Load data
    participant_data = pd.read_pickle(d + "/reports/extracted_features/ml/%s.pickle" % (p))
    participant_features = participant_data['objective']
    rfecv_results = pd.read_pickle(d + "/reports/feature_selection/rfecv/%s.pickle" % (p))
    rfecv_results_iteration = rfe_results[rs]
    # Which features are relevant for the selected participant?
    # Build dict with names of selected features, as per RFECV analysis
    features_names_dimensions = {}
    for dim in dimensions:
        dimension_results = rfecv_results_iteration[dim]
        features_names = extract_selected_features_names(dimension_results)
        features_names_dimensions[dim] = features_names

    # Build dictionary with data of the selected features
    nested_dict = lambda: defaultdict(nested_dict)
    selected_features = nested_dict()
    for dim in dimensions:
        relevant_features_dim = list(features_names_dimensions[dim].keys())
        for t in trials:
            for f in relevant_features_dim:
                if f not in ['relative_power_spectral_density', 'frontal_asymmetry']:
                    relevant_electrodes = flatten_list(features_names_dimensions[dim][f])
                    for e in relevant_electrodes:
                        selected_features[dim][t][f][e] = participant_features[t][f][e]
                if f == 'relative_power_spectral_density':
                    relevant_bands = features_names_dimensions[dim][f]
                    for b in relevant_bands:
                        relevant_electrodes = flatten_list(features_names_dimensions[dim][f][b])
                        for e in relevant_electrodes:
                            selected_features[dim][t][f][b][e] = participant_features[t][f][b][e]
                if f == 'frontal_asymmetry':
                    relevant_bands = flatten_list(features_names_dimensions[dim][f])
                    for b in relevant_bands:
                        selected_features[dim][t][f][b] = participant_features[t][f][b]
                else:
                    continue

    # Select trials that were not used in the RFECV analysis. This is necessary to prevent double-dipping.
    participant_ml_data = subset_trials_ml(p, selected_features, rs)
    return participant_ml_data


if __name__ == "__main__":
    select_features_rfecv()