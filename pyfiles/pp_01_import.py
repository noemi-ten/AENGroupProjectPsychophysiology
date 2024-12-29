import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from opensignalsreader import OpenSignalsReader
import os

## Import all files
# Parameters
sourceDataFolder = r"C:/Users/noemi/ProjectPsychophisiology/ProjectPsychophysiologyGroup/AENGroupProjectPsychophysiology/source-data"
rawDataFolder = r"C:/Users/noemi/ProjectPsychophisiology/ProjectPsychophysiologyGroup/AENGroupProjectPsychophysiology/raw-data"

participants = ['sub-1', 'sub-2', 'sub-3']
tasks = ['baseline', 'spiderhand', 'spidervideo']
#sessions = ['ground', 'high']

for pi in participants:
    for ti in tasks:
        #for si in sessions:

        # assemble file name   '-' + si +
        filename = sourceDataFolder + '/' + pi + '_' + ti + '.txt'

        # skip the missing file
        if filename == sourceDataFolder + '/sub-02_base-high.txt':
            print('skipping sub-02 base high file')
            continue

        # Convert all other files
        acq = OpenSignalsReader(filename)

        # Access the processed ECG signal and print the first 5 elements
        ecg_signal = acq.signal('ECG')
        print(ecg_signal[:5])

        # Access the processed EDA signal and print the first 5 elements
        eda_signal = acq.signal('XEDA')
        print(eda_signal[:5])

        ## Save data in a .csv format   '-' + si +
        output_filename_ecg = rawDataFolder + '/' + pi + '_' + ti + '_ecg.csv'
        output_filename_eda = rawDataFolder + '/' + pi + '_' + ti + '_eda.csv'

        # Save the NumPy array to a CSV file
        np.savetxt(output_filename_ecg, ecg_signal, delimiter=',', header='ECG')
        np.savetxt(output_filename_eda, eda_signal, delimiter=',', header='EDA')
        print(f"Wrote files {output_filename_ecg} and {output_filename_eda}")