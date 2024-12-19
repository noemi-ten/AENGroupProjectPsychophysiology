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
raw_data_folder = 'C:/Users/seinj/Teaching/Data/raw-data/'
results_folder = 'C:/Users/seinj/Teaching/Results/'
os.makedirs(results_folder, exist_ok=True)

# parameters
participants = ['sub-01', 'sub-02']
tasks = ['base', 'walk']
sessions = ['ground', 'high']

all_results = []

for pi in participants:
    for ti in tasks:
        for si in sessions:

            # assemble file name
            filename = raw_data_folder + '/' + pi + '_' + ti + '-' + si + '_ecg.csv'

            # skip the missing file
            if filename == raw_data_folder + '/sub-02_base-high_ecg.csv':
                print('skipping sub-02 base high file')
                continue
            print('reading in ' + filename)

            # read in the data in respective conditions
            subdata = pd.read_csv(filename, header=None, names=['ECG'], skiprows=1)

            # Extract the single column as a vector
            ecg_data = subdata['ECG'].values

            # process the full time window
            signals_full, info = nk.ecg_process(ecg_data, sampling_rate=1000)

            # select segment to plot
            ecg_signals = signals_full  # .iloc[50000:90000]

            # Following is modification of ecg_plot()
            # https://neuropsychology.github.io/NeuroKit/_modules/neurokit2/ecg/ecg_plot.html#ecg_plot

            # Extract R-peaks (take those from df as it might have been cropped)
            if "ECG_R_Peaks" in ecg_signals.columns:
                info["ECG_R_Peaks"] = np.where(ecg_signals["ECG_R_Peaks"] == 1)[0]

            # Prepare figure and set axes.
            gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[2 / 3, 1 / 3])
            fig = plt.figure(constrained_layout=False)
            ax0 = fig.add_subplot(gs[0, :-1])
            ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
            ax2 = fig.add_subplot(gs[:, -1])

            # Plot signals
            phase = None
            if "ECG_Phase_Ventricular" in ecg_signals.columns:
                phase = ecg_signals["ECG_Phase_Ventricular"].values

            ax0 = _ecg_peaks_plot(
                ecg_signals["ECG_Clean"].values,
                info=info,
                sampling_rate=info["sampling_rate"],
                raw=ecg_signals["ECG_Raw"].values,
                quality=ecg_signals["ECG_Quality"].values,
                phase=phase,
                ax=ax0,
            )

            # Plot Heart Rate
            ax1 = _signal_rate_plot(
                ecg_signals["ECG_Rate"].values,
                info["ECG_R_Peaks"],
                sampling_rate=info["sampling_rate"],
                title="Heart Rate",
                ytitle="Beats per minute (bpm)",
                color="#FF5722",
                color_mean="#FF9800",
                color_points="#FFC107",
                ax=ax1,
            )

            # Plot individual heart beats
            ax2 = ecg_segment(
                ecg_signals,
                info["ECG_R_Peaks"],
                info["sampling_rate"],
                show="return",
                ax=ax2,
            )

            ax0.set_position([0.1, 0.9, 0.8, 0.2])
            ax1.set_position([0.1, 0.5, 0.8, 0.2])
            ax2.set_position([0.1, 0.1, 0.8, 0.2])

            # Save the current figure to a file
            figure_filename = results_folder + f'/{pi}_{ti}_{si}_ecg_nk.png'
            plt.savefig(figure_filename, bbox_inches='tight', pad_inches=0.1)  # Save the current active plot as a PNG file
            print(f"Saved figure to {figure_filename}")

            # Close the plot to free memory after saving
            plt.close()

            # process full length interval related data
            results = nk.ecg_intervalrelated(signals_full, sampling_rate=1000)
            print(results)

            # Append the results to the list with participant and condition as metadata
            results['Participant'] = pi
            results['Condition'] = ti + '_' + si
            all_results.append(results)

# Concatenate all the results into a single DataFrame
final_results = pd.concat(all_results, ignore_index=True)

# Save the concatenated DataFrame to a CSV file
output_filename = results_folder + 'ecg_results.csv'
final_results.to_csv(output_filename, index=False)

print(f"Saved results to {output_filename}")