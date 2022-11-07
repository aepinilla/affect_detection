"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split

from src.helper import get_rfecv_data
from src.settings import d, dimensions, participants_codes, random_states_list


def conduct_rfecv(p):
    # Load data
    participant_data = pd.read_pickle(d + "/reports/extracted_features/ml/%s.pickle" % (p))
    participant_features = participant_data['objective']
    rfecv_all_trials = {}
    for i in random_states_list:
        print('Using RFECV for selecting features extracted from participant ' + p + ', iteration ' + str(i))
        rfecv_data = get_rfecv_data(i, participant_features, p)
        # Select features for each dimension
        rfecv_features = {}
        for dim in dimensions:
            dim_data = rfecv_data[dim]
            features = dim_data['features']
            labels = dim_data['labels']
            estimator = RandomForestClassifier()
            selector = RFECV(estimator=estimator, scoring='accuracy', cv=4, step=5)
            selector = selector.fit(features, np.ravel(labels))
            rfecv_features[dim] = features.columns[selector.support_]

        rfecv_all_trials[i] = rfecv_features

    # Export RFE results
    rfecv_results_path = d + '/reports/feature_selection/rfecv/' + p + '.pickle'
    with open(rfecv_results_path, 'wb') as handle:
        pickle.dump(rfecv_all_trials, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    conduct_rfecv()