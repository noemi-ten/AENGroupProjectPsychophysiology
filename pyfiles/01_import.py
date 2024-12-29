#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from opensignalsreader import OpenSignalsReader
import os


# In[45]:


import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
sourceDataFolder = '/Users/erwin/Documents/ProjectPsychophysiologyData/source-data'
rawDataFolder = '/Users/erwin/Documents/ProjectPsychophysiologyData/raw-data/'
participants = ['sub-1', 'sub-2', 'sub-3']
tasks = ['baseline', 'spiderhand', 'spidervideo']

# Ensure output directory exists
if not os.path.exists(rawDataFolder):
    os.makedirs(rawDataFolder)

# Loop through participants and tasks
for pi in participants:
    for ti in tasks:
        filename = os.path.join(sourceDataFolder, f"{pi}_{ti}.txt")
        print(f"Processing: {filename}")

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue

        try:
            # Read the file and skip the header
            with open(filename, 'r') as f:
                # Skip header lines (assuming they start with '#')
                header_lines = []
                line = f.readline()
                while line.startswith('#'):
                    header_lines.append(line.strip())
                    line = f.readline()

                # Now read the data into a NumPy array
                data = np.loadtxt([line] + f.readlines())

            # Extract ECG (A1) and EDA (A2) signals
            ecg_signal_raw = data[:, 5]  # Column index for A1 (ECG)
            eda_signal_raw = data[:, 6]  # Column index for A2 (EDA)

            # Scaling for ECG (A1) and EDA (A2) based on 10-bit resolution
            # ECG scaling: approximately 0.00195 mV per ADC unit
            ecg_signal = ecg_signal_raw * 0.00195  # Scale to mV (millivolts)

            # EDA scaling: approximately 0.0391 µS per ADC unit
            eda_signal = eda_signal_raw * 0.0391  # Scale to µS (microsiemens)

            # Print the first 5 values for verification
            print(f"ECG Signal (First 5 values): {ecg_signal[:5]}")
            print(f"EDA Signal (First 5 values): {eda_signal[:5]}")

            # Plot ECG and EDA signals
            plt.figure(figsize=(12, 6))

            # Plot ECG
            plt.subplot(2, 1, 1)
            plt.plot(ecg_signal, label='ECG (A1)')
            plt.title(f"{pi} - {ti} - ECG Signal")
            plt.xlabel('Time (samples)')
            plt.ylabel('ECG (mV)')
            plt.legend()

            # Plot EDA
            plt.subplot(2, 1, 2)
            plt.plot(eda_signal, label='EDA (A2)', color='red')
            plt.title(f"{pi} - {ti} - EDA Signal")
            plt.xlabel('Time (samples)')
            plt.ylabel('EDA (µS)')
            plt.legend()

            # Set the y-axis range for EDA (for sanity check, you can limit it to 0-40 µS)
            plt.subplot(2, 1, 2)
            plt.ylim(0, 45)  # Limit EDA to 40 µS max

            # Show the plots
            plt.tight_layout()
            plt.show()

            # Save the signals to CSV files
            output_filename_ecg = os.path.join(rawDataFolder, f"{pi}_{ti}_ecg.csv")
            output_filename_eda = os.path.join(rawDataFolder, f"{pi}_{ti}_eda.csv")

            np.savetxt(output_filename_ecg, ecg_signal, delimiter=',', header='ECG', comments='')
            np.savetxt(output_filename_eda, eda_signal, delimiter=',', header='EDA', comments='')
            print(f"Saved ECG signal to {output_filename_ecg}")
            print(f"Saved EDA signal to {output_filename_eda}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")


# In[ ]:




