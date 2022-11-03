"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from multiprocessing import Pool

from src.compare_methods import compare_methods
from src.process_data import process_data
from src.settings import participants_codes


def main():
    # Process data using multiprocessing library (20 participants are run in parallel)
    with Pool(1) as pl:
        pl.map(process_data, participants_codes)

    # Compare accuracy of classifiers built with features selected using each feature selection method.
    compare_methods()


if __name__ == "__main__":
    main()