#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from opensignalsreader import OpenSignalsReader
import os


# In[26]:


# Parameters
sourceDataFolder = '/Users/erwin/Documents/ProjectPsychophysiologyData/source-data'
rawDataFolder = '/Users/erwin/Documents/ProjectPsychophysiologyData/raw-data/'
participants = ['sub-1', 'sub-2', 'sub-3']
tasks = ['baseline', 'spiderhand', 'spidervideo']

# Ensure output directory exists
if not os.path.exists(rawDataFolder):
    os.makedirs(rawDataFolder)

for pi in participants:
    for ti in tasks:
        
            # assemble file name 
            filename = sourceDataFolder + '/' + pi + '_' + ti + '.txt'
            
            # Convert all other files 
            acq = OpenSignalsReader(filename, show=True)
            
            # Access the processed ECG / EDA signal and print the first 5 elements
            ecg_signal = acq.signal('ECG') 
            print(ecg_signal[:5]) 
            eda_signal = acq.signal('AEDA') #renamed to AEDA because of glitch
            print(eda_signal[:5]) 
        
            ## Save data in a .csv format 
            output_filename_ecg = rawDataFolder + '/' + pi + '_' + ti + '_ecg.csv'
            output_filename_eda = rawDataFolder + '/' + pi + '_' + ti + '_eda.csv'
        
            # Save the NumPy array to a CSV file
            np.savetxt(output_filename_ecg, ecg_signal, delimiter=',', header='ECG')
            np.savetxt(output_filename_eda, eda_signal, delimiter=',', header='EDA')
        
            print(f"Wrote files {output_filename_ecg} and {output_filename_eda}")


# In[ ]:




