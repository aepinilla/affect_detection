import os

# Directory path
d = os.path.dirname(os.getcwd()) + '/affect_detection'

# Define sampling frequency
fs = 128

# Define window size for Welch's method
number_cycles = 32
lowest_frequency = 4
welch_window_size = (number_cycles / lowest_frequency) * fs

# Define window size for moving window
moving_window_size = int((number_cycles / lowest_frequency) * fs * 2)

# Define bands
bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']

# Define names of EEG electrode sites
electrode_sites = ['F3', 'F4', 'P3', 'P4']

# Pilot experiment videos
exp_videos = list(range(1, 17))
# exp_videos = list(range(1, 2))


exp_participant_codes = ['3I6EY',
                         '6HARB',
                         'AY9SI',
                         #'DODE8', #Outlier
                         'GLJO8',
                         #'GNIE1', #Outlier
                         #'J7BUL',#Corrupted data
                         #'JB584',#Corrupted data
                         'KNY2Z',
                         'MJC27',
                         'MRB58',
                         'NJL7V',
                         #'PJGHY', #Outlier
                         'QPLQF',
                         #'RSC25', #Outlier
                         'SDE14',
                         'SWLFB',
                         #'SXZNO', #Outlier
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