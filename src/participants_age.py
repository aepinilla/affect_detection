"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

"""
Calculate age of participants per gender.
"""

import pandas as pd
from src.helper import remove_outliers
from src.settings import corrupted_participants, d


def participants_age(outlier_participants):
    # Read demgoraphics data file
    data = pd.read_csv(d + '/data/subjective/demographics.csv')
    non_corrupted = data[~data['Participant Code'].isin(corrupted_participants)]
    non_outliers = non_corrupted[~non_corrupted['Participant Code'].isin(outlier_participants)]

    demographics = pd.DataFrame.from_dict({
        'age_min': non_outliers['What is your age?'].min(),
        'age_max': non_outliers['What is your age?'].max(),
        'age_mean': round(non_outliers['What is your age?'].mean(), 2),
        'age_sd': round(non_outliers['What is your age?'].std(), 2),
        'gender_count': non_outliers.groupby(['What is your gender?']).size()
    })

    demographics.to_csv(d + '/reports/participants_age.csv')


if __name__ == "__main__":
    participants_age()