import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import os as os

# Paths to folders
raw_data_folder = 'C:/Users/seinj/Teaching/Data/raw-data/'
results_folder = 'C:/Users/seinj/Teaching/Results/'
os.makedirs(results_folder, exist_ok=True)

# parameters
participants = ['sub-01']
tasks = ['base', 'walk']
sessions = ['ground', 'high']

all_results = []

for pi in participants:
    for ti in tasks:
        for si in sessions:

            # assemble file name
            filename = raw_data_folder + '/' + pi + '_' + ti + '-' + si + '_eda.csv'

            # skip the missing file
            if filename == raw_data_folder + '/sub-02_base-high_eda.csv':
                print('skipping sub-02 base high file')
                continue
            print('reading in ' + filename)

            # read in the data in respective conditions
            subdata = pd.read_csv(filename, header=None, names=['EDA'], skiprows=1)

            # Extract the single column as a vector
            eda_data = subdata['EDA'].values

            # process the full time window
            signals_full, info = nk.eda_process(eda_data, sampling_rate=1000)

            if filename != raw_data_folder + '/sub-02_base-ground_eda.csv': # The exception is made for this file because this file contains no bursts
                # plot results
                nk.eda_plot(signals_full, info)

                # Save the current figure to a file
                figure_filename = results_folder + f'/{pi}_{ti}_{si}_eda_nk.png'
                plt.savefig(figure_filename, bbox_inches='tight',
                            pad_inches=0.1)  # Save the current active plot as a PNG file
                print(f"Saved figure to {figure_filename}")

            # summarize the number of activation and mean amplitude for the given interval
            results = nk.eda_analyze(signals_full, method="interval-related")
            print(results)

            # Append the results to the list with participant and condition as metadata
            results['Participant'] = pi
            results['Condition'] = ti + '_' + si
            all_results.append(results)

# Concatenate all the results into a single DataFrame
final_results = pd.concat(all_results, ignore_index=True)

# Save the concatenated DataFrame to a CSV file
output_filename = results_folder + 'eda_results.csv'
final_results.to_csv(output_filename, index=False)

print(f"Saved results to {output_filename}")
