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


def conduct_rfecv():
    for p in participants_codes:
        print('Conducting RFECV for participant ' + p)
        # Load data
        participant_data = pd.read_pickle(d + "/reports/extracted_features/ml/%s.pickle" % (p))
        participant_features = participant_data['objective']
        rfecv_all_trials = {}
        for i in random_states_list:
            rfecv_data = get_rfecv_data(i, participant_features, p)
            # Select features for each dimension
            rfecv_features = {}
            for dim in dimensions:
                print('Selecting features for ' + dim + ' dimension')
                dim_data = rfecv_data[dim]
                features = dim_data['features']
                labels = dim_data['labels']
                # Split in training and testing set
                x_train, x_test, y_train, y_test = train_test_split(features, labels, train_size=0.3, random_state=i)
                # Run Recursive Feature Elimination with Cross Validation
                estimator = RandomForestClassifier()
                rfecv = RFECV(estimator=estimator, step=5, scoring='accuracy')   #5-fold cross-validation
                rfecv = rfecv.fit(x_train, np.ravel(y_train, order='C'))
                rfecv_features[dim] = x_train.columns[rfecv.support_]

            rfecv_all_trials[i] = rfecv_features

        # Export RFE results
        rfecv_results_path = d + '/reports/feature_selection/rfecv/' + p + '.pickle'
        with open(rfecv_results_path, 'wb') as handle:
            pickle.dump(rfecv_all_trials, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    conduct_rfecv()