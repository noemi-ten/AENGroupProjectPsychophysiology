#!/usr/bin/env python
# coding: utf-8

# In[3]:


import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import numpy as np
import os as os

from neurokit2.misc import NeuroKitWarning
from neurokit2.signal.signal_rate import _signal_rate_plot
from neurokit2.ecg.ecg_peaks import _ecg_peaks_plot
from neurokit2.ecg.ecg_segment import ecg_segment

# Paths to folders
raw_data_folder = '/Users/erwin/Documents/ProjectPsychophysiologyData/raw-data/'
results_folder = '/Users/erwin/Documents/ProjectPsychophysiologyData/results/'

# Parameters
participants = ['sub-1', 'sub-2', 'sub-3']
tasks = ['baseline', 'spiderhand', 'spidervideo']

all_results = []

# Loop through participants and tasks
for pi in participants:
    for ti in tasks:
        filename = os.path.join(raw_data_folder, f"{pi}_{ti}_eda.csv")
        print(f"Processing: {filename}")

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue  # Skip to the next file if not found

        # Read in the data in respective conditions
        subdata = pd.read_csv(filename, header=None, names=['EDA'], skiprows=1)

        # Extract the single column as a vector
        eda_data = subdata['EDA'].values

        # Process the full time window
        signals_full, info = nk.eda_process(eda_data, sampling_rate=1000)

        # Plot signals
        nk.eda_plot(signals_full)
        
        # Save the current figure to a file
        figure_filename = results_folder + f'/{pi}_{ti}_eda_nk.png'
        plt.savefig(figure_filename, bbox_inches='tight', pad_inches=0.1)  # Save the current active plot as a PNG file
        print(f"Saved figure to {figure_filename}")

        # Close the plot to free memory after saving
        plt.close()

        # Process full-length interval-related data
        results = nk.eda_intervalrelated(signals_full, sampling_rate=1000)
        print(results)

        # Check if results is a valid DataFrame
        if isinstance(results, pd.DataFrame):
            # Append the results to the list with participant and condition as metadata
            results['Participant'] = pi
            results['Condition'] = ti
            all_results.append(results)
        else:
            print(f"Results for {pi} {ti} are not in DataFrame format.")

# Concatenate all the results into a single DataFrame
if all_results:
    final_results = pd.concat(all_results, ignore_index=True)

    # Save the concatenated DataFrame to a CSV file
    output_filename = results_folder + 'eda_results.csv'
    final_results.to_csv(output_filename, index=False)

    print(f"Saved results to {output_filename}")
else:
    print("No valid results to save.")


# In[ ]:




