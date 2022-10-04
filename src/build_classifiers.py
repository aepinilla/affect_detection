"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from collections import defaultdict
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.feature_selection.select_features_rfecv import select_features_rfecv
from src.feature_selection.select_features_lme import select_features_lme
from src.settings import d, dimensions, feature_selection_approaches, random_states_list


def get_metrics(approach, p, rs):
    # Load dataset
    if approach == 'lme':
        participant_data = select_features_lme(p, rs)
    if approach == 'rfecv':
        participant_data = select_features_rfecv(p, rs)

    nested_dict = lambda: defaultdict(nested_dict)
    participant_metrics = nested_dict()
    for dim in dimensions:
        print('Building classifier for ' + dim)
        features = participant_data[dim]['features']
        labels = participant_data[dim]['labels']

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(features, labels, train_size=0.3, random_state=rs)

        # Initialize Random Forest Classifier
        clf = RandomForestClassifier()
        # Train the model
        clf.fit(X_train, y_train)
        # Predict the response for test dataset
        y_pred = clf.predict(X_test)

        accuracy = metrics.accuracy_score(y_test, y_pred)
        precision = metrics.precision_score(y_test, y_pred)
        recall = metrics.recall_score(y_test, y_pred)
        f1_score = metrics.f1_score(y_test, y_pred)

        participant_metrics[dim]['accuracy'] = accuracy
        participant_metrics[dim]['precision'] = precision
        participant_metrics[dim]['recall'] = recall
        participant_metrics[dim]['f1_score'] = f1_score

    return participant_metrics


def build_classifiers(p):
    # Build classifiers with each feature selection approach
    print('Building classifiers for participant ' + p)
    for approach in feature_selection_approaches:
        print('Using features obtained with ' + approach + ' analysis')
        # Build dict with each random state (10 different random states)
        participant_metrics_dict = {}
        for rs in random_states_list:
            print('Using random state ' + str(rs))
            participant_metrics_dict[rs] = pd.DataFrame.from_dict(get_metrics(approach, p, rs))

        participant_metrics_df = pd.concat(participant_metrics_dict)
        participant_metrics_df.to_csv(d + '/reports/metrics/%s/' % (approach) + p + '.csv')


if __name__ == "__main__":
    build_classifiers()