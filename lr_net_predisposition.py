import os, sys
sys.path.append('../')

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from settings import exp_participant_codes

# Define working directory
d = os.path.dirname(os.getcwd())

# Run once per participant
all_participants = []
for p in exp_participant_codes:
    print('Analysing participant %s' % (p))
    participant_features = pd.read_csv(d + '/affect_detection/features/%s_features.csv' % (p))
    # Parietal mean features
    pm = participant_features[
        ['participant', 'video_id', 'timestamp', 'band', 'parietal_mean', 'net_predisposition_type']]
    # Parietal gamma
    parietal_gamma = pm.loc[(pm['band'] == 'gamma')]
    parietal_gamma = parietal_gamma.drop(['band'], axis=1)
    parietal_gamma.columns = ['participant', 'video_id', 'timestamp', 'parietal_gamma_power', 'net_predisposition_type']
    # Net predisposition features
    net_predisposition_features = parietal_gamma.copy()
    # Participant's net predisposition data
    net_predisposition = net_predisposition_features[['net_predisposition_type', 'parietal_gamma_power']]

    data = net_predisposition.iloc[:, 1].values.reshape(-1, 1)
    labels = net_predisposition.iloc[:, 0].values

    X_train, X_test, y_train, y_test = train_test_split(data, labels, train_size=0.2, random_state=42)

    # instantiate the model (using the default parameters)
    logreg = LogisticRegression()

    # fit the model with data
    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)

    # import the metrics class
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

    # class_names = [0, 1]  # name  of classes
    # fig, ax = plt.subplots()
    # tick_marks = np.arange(len(class_names))
    # plt.xticks(tick_marks, class_names)
    # plt.yticks(tick_marks, class_names)
    # # create heatmap
    # sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
    # ax.xaxis.set_label_position("top")
    # plt.tight_layout()
    # plt.title('Confusion matrix', y=1.1)
    # plt.ylabel('Actual label')
    # plt.xlabel('Predicted label')
    # plt.show()

    # Calculate metrics of current iteration
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1_score = 2 * ((precision * recall) / (precision + recall))
    valence_metrics = [accuracy, precision, recall, f1_score]
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
all_participants_df.to_csv(d + '/deap/results/metrics/lr_net_predisposition.csv', index=False)

means = all_participants_df.mean()
std = all_participants_df.std()

print(round(means, 4))
print(round(std, 4))
