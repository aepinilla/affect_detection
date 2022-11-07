"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from multiprocessing import Pool

from src.compare_methods import compare_methods
from src.create_reports_dir import create_reports_dir
from src.process_data import process_data
from src.settings import participants_codes


def main():
    # Generate directory for storing reports
    create_reports_dir()

    # Process data using multiprocessing library (10 participants are run in parallel)
    with Pool(10) as pl:
        pl.map(process_data, participants_codes)

    # Compare accuracy of classifiers built with features selected using each feature selection method.
    compare_methods()


if __name__ == "__main__":
    main()