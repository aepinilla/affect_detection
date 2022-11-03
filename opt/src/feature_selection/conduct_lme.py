"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import warnings
import rpy2.robjects as robjects
from src.settings import d, feature_groups


def conduct_lme(p):
    # print('Conducting LME analysis for participant ' + p)
    for fg in feature_groups:
        r_source = robjects.r['source']
        path = d + '/opt/src/feature_selection/lme_models/lme_analysis_%s.R' % (fg)
        r_source(path)
        # Loading the function we have defined in R.
        analyse_participant_lme_function_r = robjects.globalenv['analyse_participant_lme']
        analyse_participant_lme_function_r(p, d)


if __name__ == "__main__":
    conduct_lme()