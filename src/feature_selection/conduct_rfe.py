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

from src.helper import get_rfe_data
from src.settings import d, dimensions, participants_codes, random_states_list


def conduct_rfe():
    for p in participants_codes:
        print('Conducting RFE for participant ' + p)
        # Load data
        participant_data = pd.read_pickle(d + "/reports/extracted_features/ml/%s.pickle" % (p))
        participant_features = participant_data['objective']
        rfe_all_trials = {}
        for i in random_states_list:
            rfe_data = get_rfe_data(i, participant_features, p)
            # Select features for each dimension
            rfe_features = {}
            for dim in dimensions:
                print('Selecting features for ' + dim + ' dimension')
                dim_data = rfe_data[dim]
                features = dim_data['features']
                labels = dim_data['labels']
                # Split in training and testing set
                x_train, x_test, y_train, y_test = train_test_split(features, labels, train_size=0.3, random_state=i)
                # Run Recursive Feature Elimination with Cross Validation
                estimator = RandomForestClassifier()
                rfecv = RFECV(estimator=estimator, step=5, scoring='accuracy')   #5-fold cross-validation
                rfecv = rfecv.fit(x_train, np.ravel(y_train, order='C'))
                rfe_features[dim] = x_train.columns[rfecv.support_]

            rfe_all_trials[i] = rfe_features

        # Export RFE results
        rfe_results_path = d + '/reports/feature_selection/rfe/' + p + '.pickle'
        with open(rfe_results_path, 'wb') as handle:
            pickle.dump(rfe_all_trials, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    conduct_rfe()