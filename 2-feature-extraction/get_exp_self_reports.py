# Analyse self-report questionnaires
import os, sys
import seaborn as sns; sns.set()
import pandas as pd
from settings import exp_video_ids_dict, exp_participant_codes

sys.path.append('../')
d = os.path.dirname(os.getcwd())

def get_exp_self_reports():
    self_reports_collection = []
    for p in exp_participant_codes:
        # Read data
        filename = d + '/data/pilot_exp/subjective/self_reports/%s_self_report.csv' % (p)
        psychopy_data = pd.read_csv(filename)
        self_reports = psychopy_data[['videoFile', 'likertNegativity.response', 'likertPositivity.response', 'likertArousal.response']]
        self_reports = self_reports.dropna().reset_index(drop=True)

        # Add participant code
        self_reports['participant_code'] = p

        # Create empty column for video codes
        self_reports['video_id'] = 'NaN'

        # Add video number (trial number)
        self_reports['trial'] = list(range(1, 17))

        # Assign video codes
        for key, value in exp_video_ids_dict.items():
            self_reports.loc[self_reports['videoFile'] == key, 'video_id'] = value

        # Rename columns
        self_reports.columns = ['video_file', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating', 'participant', 'video_id', 'trial']

        # Add self-report to list
        self_reports_collection.append(self_reports)

    all_self_reports = pd.concat(self_reports_collection)
    all_self_reports = all_self_reports[['participant', 'video_id', 'trial', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]

    return all_self_reports