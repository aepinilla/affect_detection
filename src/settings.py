"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

import os


# Participants with corrupted data
corrupted_data = ['Y8ZJQ', 'J7BUL', 'JB584']

# Directory path
d = os.path.dirname(os.getcwd()) + '/affect_detection'

# Affective dimensions
dimensions = 'negativity', 'positivity', 'net_predisposition'

# Frequency bands
eeg_bands = {'delta': (0.1, 4),
             'theta': (4, 8),
             'alpha': (8, 13),
             'beta':  (13, 30),
             'gamma': (30, 45)
             }

# Feature groups for LME analysis
feature_groups = [
    "base",
    "fa",
    "rpsd"
]

# List of extracted features
features_list = [
    'spectral_envelope',
    'zero_crossings',
    'katz_fractal_dimension',
    'hjorth_activity',
    'hjorth_movility',
    'hjorth_complexity',
    'petrosian_fractal_dimension',
    'relative_power_spectral_density',
    'frontal_asymmetry'
]

# Approaches (methods) for feature selection
feature_selection_approaches = ['lme', 'rfe']

# Define sampling frequency
fs = 128

# Ratio of trials used for feature selection and for model training/testing
fs_dataset_ratio, model_dataset_ratio = .3, .7

# The length of the data of each video is 60 seconds multiplied by the sampling frequency (fs).
# The last sample for each video is lost during the preprocessing, thus 1 is rested to the length of the video.
# The duration of each epoch in seconds
epoch_len = 60
len_epoch = (epoch_len * fs) - 1

# List of participant's codes
participants_codes = [
                     '3I6EY',
                     '6HARB', # Outlier
                     'AY9SI',
                     'DODE8', # Outlier
                     'GLJO8', # Outlier
                     'GNIE1', # Outlier
                     # 'J7BUL',# Corrupted data
                     # 'JB584',# Corrupted data
                     'KNY2Z',
                     'MJC27',
                     'MRB58',
                     'NJL7V',
                     'PJGHY',
                     'QPLQF',
                     'RSC25',
                     'SDE14',
                     'SWLFB',
                     'SXZNO',
                     'TXNOY',
                     'UVBY3',
                     'VHY9N',
                      # 'Y8ZJQ', #Corrupted data
                      'YOO7M' # Outlier
                      ]

# List of values used for random state (for replicable results)
random_states_list = list(range(1, 11))

# Define window size for Welch's method
# Size of the sliding window used for extracting the features
number_cycles = 32
lowest_frequency = 4
sliding_window_size = int(((number_cycles / lowest_frequency) * fs) * 4)

# List of trial ids
trials = list(range(1, 17))

# Dictionary with codes assigned to each video
video_ids = {
    'stims/arch_enemy__my_apocalypse.mov': 'aem',
    'stims/Benny_Benassi__Satisfaction.mov': 'bbs',
    'stims/blink_182__first_date.mov': 'blf',
    'stims/blur__song_2.mov': 'bls',
    'stims/christina_aguilera__hurt.mov': 'cah',
    'stims/dj_paul_elstak__hardcore_state_of_mind.mov': 'dph',
    'stims/gorgoroth__carving_a_giant.mov': 'goc',
    'stims/grand_archives__miniature_birds.mov': 'gam',
    'stims/james_blunt__goodbye_my_lover.mov': 'jbg',
    'stims/jason_mraz__I_am_yours.mov': 'jmi',
    'stims/madonna__rain.mov': 'mar',
    'stims/manu_chao__me_gustas_tu.mov': 'mcm',
    'stims/napalm_death__procrastination_on_the_empty_vessel.mov': 'ndp',
    'stims/sepultura__refuse_resist.mov': 'ser',
    'stims/taylor_swift__love_story.mov': 'tsl',
    'stims/the_submarines__darkest_things.mov': 'tsd'
}

# Size of the (inner) sliding window used for the Welch's method
welch_window_size = (number_cycles / lowest_frequency) * fs
