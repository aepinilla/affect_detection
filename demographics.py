"""
Calculate age of participants per gender.
"""

import os, sys
sys.path.append('../')

import pandas as pd
from settings import exp_participant_codes, exp_video_ids_dict

# Define working directory
d = os.path.dirname(os.getcwd())

# Read demgoraphic data file
data = pd.read_csv(d + '/affect_detection/data/subjective/demographics.csv')

subset = data[data['Participant Code'].isin(exp_participant_codes)]
age_min = subset['What is your age?'].min()
age_max = subset['What is your age?'].max()
age_mean = round(subset['What is your age?'].mean(), 2)
age_sd = round(subset['What is your age?'].std(), 2)
gender = subset.groupby(['What is your gender?'])
gender.count()
subset.count()


self_reports_collection = []
for p in participants:
    # Assign participant code
    participant_co = files_details[participant_idx]['participant_code']

print("d")