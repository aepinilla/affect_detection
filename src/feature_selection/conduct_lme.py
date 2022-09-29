"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import rpy2.robjects as robjects
from src.settings import d, feature_groups


def conduct_lme():
    for fg in feature_groups:
        print('Conducting LME analysis for feature group ' + fg)
        r_source = robjects.r['source']
        path = d + '/src/feature_selection/lme_models/lme_analysis_%s.R' % (fg)
        r_source(path)


if __name__ == "__main__":
    conduct_lme()