"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

"""
This technique is repeated 10 times per participant. In each iteration, data is split randomly in two subsets.
The first subset is used for feature selection. The second subset is used for training and testing the model.
This is step is necessary to avoid double dipping (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7422774/)
The current file generates random subsets of the trials used for the first and second subset.
10 collections of indices are generated: one for each iteration.
"""

import pandas as pd

from src.settings import d, random_states_list
from src.helper import get_split_indices, self_reports


def random_indices(p):
    print('Generating indices for random trial selection of participant ' + p)
    all_self_reports = self_reports()
    participant_self_reports = all_self_reports.loc[all_self_reports.participant == p]

    random_indices_collection = []
    for rst in random_states_list:
        indices = get_split_indices(participant_self_reports, rst)
        indices_df = pd.DataFrame.from_dict(indices)
        indices_df['iteration'] = rst
        random_indices_collection.append(indices_df)

    participant_random_indices = pd.concat(random_indices_collection)
    participant_random_indices.to_csv(d + '/reports/random_indices/' + p + '.csv', index=False)


if __name__ == "__main__":
    random_indices()