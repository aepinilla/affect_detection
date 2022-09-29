"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from src.analyse_features import analyse_features
from src.build_classifiers import build_classifiers
from src.compare_methods import compare_methods
from src.extract_features import extract_features
from src.lme_structure import lme_structure
from src.participants_age import participants_age
from src.random_indices import random_indices
from src.settings import participants_codes


def main():
    # Generate random indices, extract features, and adjust extracted features to LME format.
    for p in participants_codes:
        random_indices(p)
        extract_features(p)
        lme_structure(p)
    # Analyse features using LME and RFE
    analyse_features()
    # Build classification models with selected features
    for p in participants_codes:
        build_classifiers(p)
    # Compare accuracy of classifiers built with features selected using each feature selection method.
    compare_methods()
    # Calculate participants' age for reporting in manuscript.
    participants_age()


if __name__ == "__main__":
    main()