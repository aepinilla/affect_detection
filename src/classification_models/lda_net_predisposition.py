import os, sys
sys.path.append('../')

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from settings import exp_participant_codes

# Define working directory
d = os.path.dirname(os.getcwd())

# Run once per participant
all_participants = []
for p in exp_participant_codes:
    print('Analysing participant %s' % (p))
    participant_features = pd.read_csv(d + '/affect_detection/features/%s_features.csv' % (p))
    # Parietal mean features
    pm = participant_features[['participant', 'video_id', 'timestamp', 'band', 'parietal_mean', 'net_predisposition_type']]
    # Parietal gamma
    parietal_gamma = pm.loc[(pm['band'] == 'gamma')]
    parietal_gamma = parietal_gamma.drop(['band'], axis=1)
    parietal_gamma.columns = ['participant', 'video_id', 'timestamp', 'parietal_gamma_power', 'net_predisposition_type']
    # Net predisposition features
    net_predisposition_features = parietal_gamma.copy()
    # Participant's net predisposition data
    net_predisposition = net_predisposition_features[['net_predisposition_type', 'parietal_gamma_power']]

    X = net_predisposition.iloc[:, 1].values.reshape(-1, 1)
    y = net_predisposition.iloc[:, 0].values

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
all_participants_df.to_csv(d + '/deap/results/metrics/lda_net_predisposition.csv', index=False)

means = all_participants_df.mean()
std = all_participants_df.std()

print(round(means, 4))
print(round(std, 4))
