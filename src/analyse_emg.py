from biosppy import utils
from src.settings import d

def analyse_emg(p):
    print("Analysing EMG data for participant " + p)
    emg_raw_data = (d + '/data/objective/csv/emg/%s_eeg.csv' % (p))

    print('')