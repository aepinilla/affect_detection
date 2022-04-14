import pandas as pd
import seaborn as sns; sns.set()

from .settings import exp_video_ids_dict, exp_participant_codes, d


def self_reports():
    self_reports_collection = []
    for p in exp_participant_codes:
        # Read data
        filename = d + '/data/subjective/self_reports/%s_self_report.csv' % (p)
        psychopy_data = pd.read_csv(filename)
        self_report = psychopy_data[['videoFile', 'likertNegativity.response', 'likertPositivity.response', 'likertArousal.response']]
        self_report = self_report.dropna().reset_index(drop=True)

        # Add participant code
        self_report['participant_code'] = p

        # Create empty column for video codes
        self_report['video_id'] = 'NaN'

        # Add video number (trial number)
        self_report['trial'] = list(range(1, 17))

        # Assign video codes
        for key, value in exp_video_ids_dict.items():
            self_report.loc[self_report['videoFile'] == key, 'video_id'] = value

        # Rename columns
        self_report.columns = ['video_file', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating', 'participant', 'video_id', 'trial']

        # Add self-report to list
        self_reports_collection.append(self_report)

    all_self_reports = pd.concat(self_reports_collection)
    all_self_reports = all_self_reports[['participant', 'video_id', 'trial', 'negativity_rating', 'positivity_rating', 'net_predisposition_rating']]

    # Define video types
    all_self_reports.loc[all_self_reports['negativity_rating'] >= 5, 'negativity_type'] = 1
    all_self_reports.loc[all_self_reports['negativity_rating'] < 5, 'negativity_type'] = 0

    all_self_reports.loc[all_self_reports['positivity_rating'] >= 5, 'positivity_type'] = 1
    all_self_reports.loc[all_self_reports['positivity_rating'] < 5, 'positivity_type'] = 0

    all_self_reports.loc[all_self_reports['net_predisposition_rating'] >= 5, 'net_predisposition_type'] = 1
    all_self_reports.loc[all_self_reports['net_predisposition_rating'] < 5, 'net_predisposition_type'] = 0

    return all_self_reports


if __name__ == "__main__":
    self_reports()