import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read data from the file
RC = 515
distance = 100
filename = "CLR_matrix_100m_RC" + str(RC) + "_weight.txt"

# Assuming your text file has no header and is comma-separated
# Provide column names explicitly
column_names = ['SimulationNumber', 'Distance', 'CLR', 'Pkeep', 'Weight']
df = pd.read_csv(filename, delimiter=',', names=column_names)

# Filter data where 'CLR' is greater than 0 and 'Distance' is less than or equal to the specified distance
filtered_df = df[(df['CLR'] >= 0) & (df['Distance'] <= distance)]

# Group by 'Distance' and 'Pkeep', calculate mean of 'PAoI' and 'Weight' for each group
result_df = filtered_df.groupby(['Distance', 'Pkeep'], as_index=False).agg({'CLR': 'mean', 'Weight': 'mean'})

result_df.sort_values(by=['Pkeep', 'Distance'], inplace=True)

# Write the result to a new text file
output_file_path = "CLR_Weight_matrix_mean_RC" + str(RC) + ".txt"
result_df.to_csv(output_file_path, sep=',', index=False)

data = np.genfromtxt(output_file_path, delimiter=',', names=['Distance', 'Pkeep', 'CLR', 'Weight'])

# Filter out rows where Pkeep is zero
filtered_data = data[(data['CLR'] > 0) & (data['Distance'] <= distance)]

# Calculate average PAoI per Distance for each Pkeep
pkeep_values = np.unique(filtered_data['Pkeep'])
average_paio_per_distance = []


for pkeep in pkeep_values:
    weighted_average_paio = 0
    total_weight = 0
    subset_data = filtered_data[filtered_data['Pkeep'] == pkeep]
    subset_size = len(subset_data)
    
    if subset_size > 0:
        weighted_average_paio += np.sum(subset_data['CLR'] * subset_data['Weight'])
        total_weight += np.sum(subset_data['Weight'])

    if total_weight > 0:
        final_weighted_average = weighted_average_paio / total_weight
        average_paio_per_distance.append((pkeep, final_weighted_average))
    else:
        print("No valid data points for calculation.")
'''
for pkeep in pkeep_values:
    subset_data = filtered_data[filtered_data['Pkeep'] == pkeep]
    average_paio = np.mean(subset_data['PAoI'])
    average_paio_per_distance.append((pkeep, average_paio*1000))
'''
# Unpack the result for plotting
pkeep_values, average_paio_values = zip(*average_paio_per_distance)

# Plot PAoI as a function of Pkeep
plt.plot(pkeep_values, average_paio_values, marker='o', linestyle='-')

# Add labels and title
plt.xlabel('Pkeep')
plt.ylabel('CLR')

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16
#plt.ylim(0, 1)
plt.rc('font', size=MEDIUM_SIZE, family='Times New Roman')          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.grid()
plt.title('Average CLR as a function of Pkeep. Distance=<' + str(distance))
plt.savefig('meanCLR_vs_Pkeep_100m_Distance' + str(distance) +'RC'+ str(RC)  +'.png')
plt.savefig('meanCLR_vs_Pkeep_100m_Distance' + str(distance) +'RC'+ str(RC)  +'.eps')
# Show the plot
plt.show()

# Sort data by 'Pkeep' and then by 'Distance'
sorted_data = np.sort(filtered_data, order=['Pkeep', 'Distance'])

# Get unique values of 'Pkeep'
pkeep_values = np.unique(sorted_data['Pkeep'])

# Plot the curves for different 'Pkeep' values
for pkeep in pkeep_values:
    subset_data = sorted_data[sorted_data['Pkeep'] == pkeep]
    if pkeep == 0.99:
        plt.plot(subset_data['Distance'], subset_data['CLR'], label=f'Pkeep = {pkeep}', marker='o')
    else:
        plt.plot(subset_data['Distance'], subset_data['CLR'], label=f'Pkeep = {pkeep}')


plt.rc('font', size=MEDIUM_SIZE, family='Times New Roman')          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.grid()
plt.ylim(0, 1)
# Add labels and legend
plt.xlabel('Distance')
plt.ylabel('CLR')
plt.legend()
plt.title('CLR as a function of Distance. Distance=<' + str(distance))

plt.savefig('CLR_vs_Distance_100m_zoom1_10pkeep_Distance' + str(distance) +'RC'+ str(RC)  +'.png')
plt.savefig('CLR_vs_Distance_100m_zoom1_10pkeep_Distance' + str(distance) +'RC'+ str(RC)  +'.eps')
# Show the plot
plt.show()


# Specify the 'Pkeep' values to plot
pkeep_values_to_plot = [0, 0.2, 0.4, 0.6, 0.8]

# Plot the curves for the specified 'Pkeep' values
for pkeep in pkeep_values_to_plot:
    subset_data = sorted_data[sorted_data['Pkeep'] == pkeep]
    plt.plot(subset_data['Distance'], subset_data['CLR'], label=f'Pkeep = {pkeep}')

plt.rc('font', size=MEDIUM_SIZE, family='Times New Roman')          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.grid()
plt.ylim(0, 1)
# Add labels and legend
plt.xlabel('Distance')
plt.ylabel('CLR')
plt.legend()
plt.title('CLR as a function of Distance. Distance=<' + str(distance))

# Save the figure to a file
plt.savefig('CLR_vs_Distance_100m_Distance' + str(distance) +'RC'+ str(RC)  +'.png')
plt.savefig('CLR_vs_Distance_100m_Distance' + str(distance) +'RC'+ str(RC)  +'.eps')

# Show the plot
plt.show()
