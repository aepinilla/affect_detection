"""
Defines variables and constants that are used in other scripts.
"""

import os
d = os.path.dirname(os.getcwd())

# Define sampling frequency
fs = 128

# Define window size for Welch's method
number_cycles = 32
lowest_frequency = 4
welch_window_size = (number_cycles / lowest_frequency) * fs

# Define window size for moving window
moving_window_size = int((number_cycles / lowest_frequency) * fs)

# Define bands
bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']

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

# Define DEAP channel indexes
labels_idx = {
    'valence': 0,
    'arousal': 1
}

# Define list of videos
# Videos preprocessed using the offline approach are 0-indexed
deap_videos_offline = list(range(0, 40))

# Videos preprocessed using the online approach are 1-indexed
deap_videos_online = list(range(1, 41))

# Define list of participants
deap_participants = list(range(1,33))

# Define names of EEG electrode sites
electrode_sites = ['F3', 'F4', 'P3', 'P4']

# Pilot experiment videos
exp_videos = list(range(1, 19))

exp_participant_codes = ['3I6EY',
                         '6HARB',
                         'AY9SI',
                         'DODE8', #Outlier
                         'GLJO8',
                         'GNIE1', #Outlier
                         #'J7BUL',#Corrupted data
                         #'JB584',#Corrupted data
                         'KNY2Z',
                         'MJC27',
                         'MRB58',
                         'NJL7V',
                         'PJGHY', #Outlier
                         'QPLQF',
                         'RSC25', #Outlier
                         'SDE14',
                         'SWLFB',
                         'SXZNO', #Outlier
                         'TXNOY',
                         'UVBY3',
                         'VHY9N',
                         # 'Y8ZJQ', #Corrupted data
                         'YOO7M'
                         ]

# Define video codes
exp_video_ids_dict = {
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

# Define exp dimensions
exp_dimensions = ['negativity', 'positivity', 'net_predisposition']