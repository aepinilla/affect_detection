import os, sys
sys.path.append('../')

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from ..settings import d, exp_participant_codes


def lda_positivity():
    # Define working directory
    d = os.path.dirname(os.getcwd())

    # Run once per participant
    all_participants = []
    for p in exp_participant_codes:
        print('Analysing participant %s' % (p))
        participant_features = pd.read_csv(d + '/affect_detection/features/%s_features.csv' % (p))
        # Parietal mean features
        pm = participant_features[['participant', 'video_id', 'timestamp', 'band', 'parietal_mean', 'positivity_type']]
        # Parietal theta
        parietal_theta = pm.loc[(pm['band'] == 'theta')]
        parietal_theta = parietal_theta.drop(['band'], axis=1)
        parietal_theta.columns = ['participant', 'video_id', 'timestamp', 'parietal_theta_power', 'positivity_type']
        # Parietal alpha
        parietal_beta = pm.loc[(pm['band'] == 'alpha')]
        parietal_beta = parietal_beta.drop(['band'], axis=1)
        parietal_beta.columns = ['participant', 'video_id', 'timestamp', 'parietal_alpha_power', 'positivity_type']
        # Positivity features
        positivity_features = pd.merge(parietal_theta, parietal_beta, on=['participant', 'video_id', 'timestamp', 'positivity_type'])
        # Participant's positivity data
        positivity = positivity_features[['positivity_type', 'parietal_theta_power', 'parietal_alpha_power']]

        X = positivity.iloc[:, 1:3].values
        y = positivity.iloc[:, 0].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.2, random_state=42)

        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        lda = LDA(n_components=None)
        X_train = lda.fit_transform(X_train, y_train)
        X_test = lda.transform(X_test)

        classifier = RandomForestClassifier(max_depth=2, random_state=42)

        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        cm = confusion_matrix(y_test, y_pred)

        # Calculate metrics of current iteration
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1_score = 2*((precision*recall)/(precision+recall))
        participant_metrics = pd.DataFrame({
            'participant': p,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1-score': f1_score },
            index=[0])
        # Append results to list
        all_participants.append(participant_metrics)

    # Transform participant's results to dataframe
    all_participants_df = pd.concat(all_participants)
    all_participants_df.columns = ['participant','accuracy', 'precision', 'recall', 'f1-score']
    all_participants_df.to_csv(d + '/deap/results/metrics/lda_positivity.csv', index=False)

    # Calculate means
    means = all_participants_df.mean()
    std = all_participants_df.std()

    means_std = pd.concat([means, std], axis=1)
    means_std.columns = ['mean', 'std']
    means_std.to_csv(d + '/reports/metrics/lda_positivity_means.csv', index=True)

    print('Metrics for the positivity LDA model were exported to /reports/metrics/')


if __name__ == "__main__":
    lda_positivity()