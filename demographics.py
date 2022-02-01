"""
Calculate age of participants per gender.
"""

import os, sys
sys.path.append('../')

import pandas as pd
from settings import exp_participant_codes

# Define working directory
d = os.path.dirname(os.getcwd())

def extract_demographics():
    # Read demgoraphic data file
    data = pd.read_csv(d + '/affect_detection/data/subjective/demographics.csv')
    non_outliers = data[data['Participant Code'].isin(exp_participant_codes)]

    demographics = pd.DataFrame.from_dict({
        'age_min': non_outliers['What is your age?'].min(),
        'age_max': non_outliers['What is your age?'].max(),
        'age_mean': round(non_outliers['What is your age?'].mean(), 2),
        'age_sd': round(non_outliers['What is your age?'].std(), 2),
        'gender_count': non_outliers.groupby(['What is your gender?']).size()
    })

    demographics.to_csv('results/demographics_summary.csv')
    return demographics


if __name__ == "__main__":
    extract_demographics()