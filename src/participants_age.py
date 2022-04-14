"""
Calculate age of participants per gender.
"""

import pandas as pd
from .settings import d, exp_participant_codes


def participants_age():
    # Read demgoraphics data file
    data = pd.read_csv(d + '/data/subjective/demographics.csv')
    non_outliers = data[data['Participant Code'].isin(exp_participant_codes)]

    demographics = pd.DataFrame.from_dict({
        'age_min': non_outliers['What is your age?'].min(),
        'age_max': non_outliers['What is your age?'].max(),
        'age_mean': round(non_outliers['What is your age?'].mean(), 2),
        'age_sd': round(non_outliers['What is your age?'].std(), 2),
        'gender_count': non_outliers.groupby(['What is your gender?']).size()
    })

    demographics.to_csv(d + '/reports/participants_age.csv')
    print('Participants age was saved to reports/participants_age.csv')


if __name__ == "__main__":
    participants_age()