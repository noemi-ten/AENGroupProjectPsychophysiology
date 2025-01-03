#!/usr/bin/env python
# coding: utf-8

# # ECG Parameter extraction
# 
# Within this course, we will primarily focus on the R peaks and not other less prominent features. 
# 
# ## 1. Import packages and load the data 
# Last time, we saved the data in pkl format that preserves the structure of python variable. 

# In[5]:


import pandas as pd  
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pickle

# File path to the pickle file
derivative_folder = 'C:/Users/seinj/Teaching/Data/preprocessed-data/'
output_filename = derivative_folder + 'preprocessed_ecg.pkl'

# Load the pickle file
with open(output_filename, 'rb') as f:
    loaded_data = pickle.load(f)
    
# Display the loaded data
print(loaded_data[0])


# ## 2. Count the number of peaks 

# In[16]:


# iterate over all data within loaded_data 
for participant_data in loaded_data: 

    # extract condition and participant id for plotting
    condition_name = participant_data["condition"]
    participant_name = participant_data["participant"]
 
    # extract relevant data
    derive_sq_data = participant_data["derive_sq_data"].flatten()  # Flatten the array if it's 2D
  
    # Dynamically determine individualized threshold and distance
    signal_mean = np.mean(derive_sq_data)
    signal_std = np.std(derive_sq_data)

    # Set threshold as a multiple of the standard deviation above the mean
    indiv_threshold = signal_mean + 3 * signal_std  

    # Estimate distance based on typical ECG frequency (e.g., 60-100 bpm for resting heart rate)
    sampling_frequency = 1000  
    min_ecg_interval = 0.6  # Minimum interval in seconds between heartbeats (~100 bpm)
    indiv_distance = int(min_ecg_interval * sampling_frequency)
     
    # Apply peak detection
    peaks, _ = signal.find_peaks(derive_sq_data, height=indiv_threshold, distance=indiv_distance)  # Adjust height and distance based on signal

    # Calculate the number of beats per minute (bpm)
    peak_times = peaks / sampling_frequency  # Convert peak indices to seconds
    num_minutes = (derive_sq_data.shape[0] / sampling_frequency) / 60  # Total duration in minutes
    bpm = len(peaks) / num_minutes
    print(f"Participant: {participant_name}, Condition: {condition_name}, BPM: {bpm:.2f}")

    # Visualize only the first minute of data
    first_minute_samples = sampling_frequency * 40  
    time_axis = np.arange(first_minute_samples) / sampling_frequency  # Time axis in seconds
    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, derive_sq_data[:first_minute_samples], label="Filtered Data")
    first_minute_peaks = peaks[peaks < first_minute_samples]  # Filter peaks within the first minute
    plt.plot(first_minute_peaks / sampling_frequency, derive_sq_data[first_minute_peaks], "x", label="Detected Peaks", color="red")
    plt.title("Peak Detection " + participant_name + "_" + condition_name)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 0.0000025) 

