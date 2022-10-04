"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from src.feature_selection.conduct_lme import conduct_lme
from src.feature_selection.conduct_rfecv import conduct_rfecv

def analyse_features(p):
    conduct_lme(p)
    conduct_rfecv(p)

if __name__ == "__main__":
    analyse_features()

