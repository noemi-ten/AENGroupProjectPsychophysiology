import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from opensignalsreader import OpenSignalsReader
import os

## Import all files
# Parameters
sourceDataFolder = 'C:/Users/seinj/Teaching/Data/source-data'
rawDataFolder = 'C:/Users/seinj/Teaching/Data/raw-data'
participants = ['sub-01', 'sub-02']
tasks = ['base', 'walk']
sessions = ['ground', 'high']

for pi in participants:
    for ti in tasks:
        for si in sessions:

            # assemble file name
            filename = sourceDataFolder + '/' + pi + '_' + ti + '-' + si + '.txt'

            # skip the missing file
            if filename == sourceDataFolder + '/sub-02_base-high.txt':
                print('skipping sub-02 base high file')
                continue

            # Convert all other files
            acq = OpenSignalsReader(filename, show=True)

            # Access the processed ECG signal and print the first 5 elements
            ecg_signal = acq.signal('ECG')
            print(ecg_signal[:5])

            # Access the processed EMG signal and print the first 5 elements
            emg_signal = acq.signal('EMG')
            print(emg_signal[:5])

            ## Save data in a .csv format
            output_filename_ecg = rawDataFolder + '/' + pi + '_' + ti + '-' + si + '_ecg.csv'
            output_filename_emg = rawDataFolder + '/' + pi + '_' + ti + '-' + si + '_emg.csv'

            # Save the NumPy array to a CSV file
            np.savetxt(output_filename_ecg, ecg_signal, delimiter=',', header='ECG')
            np.savetxt(output_filename_emg, emg_signal, delimiter=',', header='EMG')
            print(f"Wrote files {output_filename_ecg} and {output_filename_emg}")

