"""
Defines variables and constants that are used in other scripts.
"""

import os
d = os.path.dirname(os.getcwd())

# Define DEAP channel indexes
channels_idx = {
    'Fp1': 1,
    'AF3': 2,
    'F3': 3,
    'F7': 4,
    'FC5': 5,
    'FC1': 6,
    'C3': 7,
    'T7': 8,
    'CP5': 9,
    'CP1': 10,
    'P3': 11,
    'P7': 12,
    'PO3': 13,
    'O1': 14,
    'Oz': 15,
    'Pz': 16,
    'Fp2': 17,
    'AF4': 18,
    'Fz': 19,
    'F4': 20,
    'F8': 21,
    'FC6': 22,
    'FC2': 23,
    'Cz': 24,
    'C4': 25,
    'T8': 26,
    'CP6': 27,
    'CP2': 28,
    'P4': 29,
    'P8': 30,
    'PO4': 31,
    'O2': 32
}

# Define sampling frequency
fs = 128

# Define window size for Welch's method
lowest_frequency = 0.5
number_cycles = 4
welch_window_size = (number_cycles / lowest_frequency) * fs

# Define bands
bands = ['alpha', 'theta']

# Define list of videos
deap_videos = list(range(0, 40))

# Define list of participants
deap_participants = list(range(1,33))

# Define names of EEG electrode sites
electrode_sites = ['F3', 'F4', 'P3', 'P4']