from src.build_classifiers import build_classifiers
from src.analyse_features import analyse_features
from src.extract_features import extract_features
from src.lme_structure import lme_structure
from src.analyse_emg import analyse_emg
from src.random_indices import random_indices


def process_data(p):
    random_indices(p)
    extract_features(p)
    lme_structure(p)
    analyse_features(p)
    build_classifiers(p)


if __name__ == '__main__':
    process_data(p)