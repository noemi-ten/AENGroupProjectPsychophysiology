#!/usr/bin/env python
# coding: utf-8

# # Visualize ECG Data with Participant Trends
# This notebook processes ECG data to visualize average heart rate across different conditions and connects individual participant data points with distinguishable lines.

# In[ ]:


# Import necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ## Load Data
# Load the `.csv` file containing the summary of ECG results.

# In[ ]:


# Paths to folders
results_folder = '/Users/erwin/Documents/ProjectPsychophysiologyData/results/'

# Load the .csv file
filename = results_folder + 'ecg_results.csv'
results = pd.read_csv(filename)

# Display the data
results.head()


# ## Filter Data by Condition
# Separate the data into `baseline`, `spiderhand`, and `spidervideo` conditions.

# In[ ]:


# Filter rows for each condition
baseline = results[results['Condition'] == 'baseline']
spiderhand = results[results['Condition'] == 'spiderhand']
spidervideo = results[results['Condition'] == 'spidervideo']

# Calculate mean values for each condition
conditions = ['Baseline', 'Spiderhand', 'Spidervideo']
averages = [baseline['ECG_Rate_Mean'].mean(), 
            spiderhand['ECG_Rate_Mean'].mean(), 
            spidervideo['ECG_Rate_Mean'].mean()]

# Display means
averages


# ## Define Plot Colors and Styles
# Set up color schemes, line styles, and marker styles for visualization.

# In[ ]:


# Define colors and styles
bar_colors = ['#fde725', '#21918c', '#440154']
scatter_colors = ['#d4c100', '#187973', '#3b0f26']
line_styles = ['-', '--', ':']  # Solid, dashed, dotted
marker_styles = ['o', 's', '^']  # Circle, square, triangle


# ## Create Plot
# Visualize the data using a bar chart with scatter plots and connect individual participant data points with distinct lines.

# In[ ]:


# Create the plot
fig, ax = plt.subplots(figsize=(6, 4))

# Bar plot
ax.bar(conditions, averages, color=bar_colors, width=0.3)

# Plot participant data
participants = results['Participant'].unique()

for i, participant in enumerate(participants):
    # Filter participant data
    participant_data = results[results['Participant'] == participant]
    participant_bpm = [
        participant_data[participant_data['Condition'] == 'baseline']['ECG_Rate_Mean'].values[0],
        participant_data[participant_data['Condition'] == 'spiderhand']['ECG_Rate_Mean'].values[0],
        participant_data[participant_data['Condition'] == 'spidervideo']['ECG_Rate_Mean'].values[0]
    ]
    
    # Plot lines and markers for participant
    ax.plot(
        conditions,
        participant_bpm,
        marker=marker_styles[i % len(marker_styles)], 
        linestyle=line_styles[i % len(line_styles)], 
        color='black', 
        label=participant,
        alpha=0.8,
        linewidth=1.5
    )

# Scatter plot for individual data points
ax.scatter([0] * len(baseline), baseline['ECG_Rate_Mean'], 
           color=scatter_colors[0], s=60, alpha=0.7, zorder=5, edgecolor='white', linewidth=1.5)
ax.scatter([1] * len(spiderhand), spiderhand['ECG_Rate_Mean'], 
           color=scatter_colors[1], s=60, alpha=0.7, zorder=5, edgecolor='white', linewidth=1.5)
ax.scatter([2] * len(spidervideo), spidervideo['ECG_Rate_Mean'], 
           color=scatter_colors[2], s=60, alpha=0.7, zorder=5, edgecolor='white', linewidth=1.5)

# Add labels, title, and legend
ax.set_ylabel('Heart Rate (bpm)')
ax.set_title('Average Heart Rate by Condition with Participant Trends')
ax.legend(loc='upper right', bbox_to_anchor=(1.4, 1), title='Participants')

# Add grid lines
ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)

# Save the plot
figure_filename = results_folder + 'ecg_summary_with_lines.png'
plt.tight_layout()
plt.subplots_adjust(right=0.7)
plt.savefig(figure_filename, bbox_inches='tight', pad_inches=0.1)

# Display the plot
plt.show()

