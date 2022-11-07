"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

"""
Convert XDF files to CSV format for faster file loading.
All credits to Robert Spang for defining the structure of this file.
"""

import numpy as np
import pyxdf
import pandas as pd

from src.settings import participants_codes, d

def column (matrix, i):
    return np.array(matrix)[:, i]

def xdf_to_csv():
    for p in participants_codes:
        # Read data
        print("Reading data from participant %s..." % (p))
        streams, fileheader = pyxdf.load_xdf(d + '/data/objective/raw/%s.xdf' % (p)) # Read streams

        # Find stream indices
        stream_brain_products = -1
        stream_gtec = -1
        stream_markers = -1
        for index in range(0, 3):
            if streams[index]['info']['name'][0] == 'BrainVision RDA':
                stream_brain_products = index
            elif streams[index]['info']['name'][0] == 'psychopy_marker_oddball':
                stream_markers = index
            elif streams[index]['info']['name'][0] == 'g.USBamp':
                stream_gtec = index

            if stream_brain_products >= 0 and stream_gtec >= 0 and stream_markers >= 0:
                break

        # Read channels
        ## Gtec channels
        ref_ch = 0
        f3_ch = 1
        f4_ch = 2
        p3_ch = 3
        p4_ch = 4
        t7_ch = 5
        t8_ch = 6
        cz_ch = 7
        zm_ch = 9
        zm_ref_ch = 10
        cs_ch = 11
        cs_ref_ch = 12

        ## Brain Products channel
        ecg_ch = 0

        ## Psychopy markers
        markers_ch = 0

        ## Read Time Stamps
        gt_time_stamps = list(streams[stream_gtec]['time_stamps'].round(decimals=2))
        bv_time_stamps = list(streams[stream_brain_products]['time_stamps'].round(decimals=2))
        markers_time_stamps = list(streams[stream_markers]['time_stamps'].round(decimals=2))

        ## Read EEG data
        ref_data = list(column(streams[stream_gtec]['time_series'], ref_ch))
        f3_data = list(column(streams[stream_gtec]['time_series'], f3_ch))
        f4_data = list(column(streams[stream_gtec]['time_series'], f4_ch))
        p3_data = list(column(streams[stream_gtec]['time_series'], p3_ch))
        p4_data = list(column(streams[stream_gtec]['time_series'], p4_ch))
        t7_data = list(column(streams[stream_gtec]['time_series'], t7_ch))
        t8_data = list(column(streams[stream_gtec]['time_series'], t8_ch))
        cz_data = list(column(streams[stream_gtec]['time_series'], cz_ch))

        eeg_dict = {'REF': ref_data,
                    'F3': f3_data,
                    'F4': f4_data,
                    'P3': p3_data,
                    'P4': p4_data,
                    'T7': t7_data,
                    'T8': t8_data,
                    'Cz': cz_data,
                    'time_stamps': gt_time_stamps}
        eeg_df = pd.DataFrame.from_dict(eeg_dict)

        ## Read EMG data
        zm_data = list(column(streams[stream_gtec]['time_series'], zm_ch))
        cs_data = list(column(streams[stream_gtec]['time_series'], cs_ch))

        emg_dict = {'ZM': zm_data,
                    'CS': cs_data,
                    'time_stamps': gt_time_stamps}
        emg_df = pd.DataFrame.from_dict(emg_dict)

        ## ECG data
        ecg_data = list(column(streams[stream_brain_products]['time_series'], ecg_ch))

        ecg_dict = {'ecg': ecg_data,
                    'time_stamps': bv_time_stamps}
        ecg_df = pd.DataFrame.from_dict(ecg_dict)

        ## Markers
        markers = pd.Series(column(streams[stream_markers]['time_series'], markers_ch))

        markers_dict = {'markers': markers,
                        'time_stamps': markers_time_stamps}

        markers_df = pd.DataFrame.from_dict(markers_dict)

        # Add markers to dataframes
        eeg_participant = pd.merge(eeg_df, markers_df, how='outer', on='time_stamps')
        emg_participant = pd.merge(emg_df, markers_df, how='outer', on='time_stamps')
        ecg_participant = pd.merge(ecg_df, markers_df, how='outer', on='time_stamps')

        # Export data
        print("Exporting data from participant %s to CSV format" % (p))
        eeg_participant.to_csv(d + '/data/objective/csv/eeg/%s_eeg.csv' % (p), index = False, header = True, sep = ',', encoding = 'utf-8')
        emg_participant.to_csv(d + '/data/objective/csv/emg/%s_emg.csv' % (p), index = False, header = True, sep = ',', encoding = 'utf-8')
        ecg_participant.to_csv(d + '/data/objective/csv/ecg/%s_ecg.csv' % (p), index = False, header = True, sep = ',', encoding = 'utf-8')


if __name__ == "__main__":
    xdf_to_csv()