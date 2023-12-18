import numpy as np
import matplotlib.pyplot as plt

distance = 100

# Read data from the first file
filename1 = "PLR_Weight_matrix_mean_RC515.txt"
data1 = np.genfromtxt(filename1, delimiter=',', names=['Distance', 'Pkeep', 'PLR'])

# Read data from the second file
filename2 = "PLR_Weight_matrix_mean_RC1.txt"  # Replace with the actual second file name
data2 = np.genfromtxt(filename2, delimiter=',', names=['Distance', 'Pkeep', 'PLR'])

# Filter out rows where Pkeep is zero for both datasets
filtered_data1 = data1[(data1['PLR'] >= 0) & (data1['Distance'] <= distance)]
filtered_data2 = data2[(data2['PLR'] >= 0) & (data2['Distance'] <= distance)]

# Calculate average PAoI per Distance for each Pkeep for both datasets
pkeep_values1 = np.unique(filtered_data1['Pkeep'])
average_paio_per_distance1 = []

for pkeep in pkeep_values1:
    subset_data = filtered_data1[filtered_data1['Pkeep'] == pkeep]
    average_paio = np.mean(subset_data['PLR'])
    average_paio_per_distance1.append((pkeep, average_paio))

pkeep_values2 = np.unique(filtered_data2['Pkeep'])
average_paio_per_distance2 = []

for pkeep in pkeep_values2:
    subset_data = filtered_data2[filtered_data2['Pkeep'] == pkeep]
    average_paio = np.mean(subset_data['PLR'])
    average_paio_per_distance2.append((pkeep, average_paio))

# Unpack the result for plotting for both datasets
pkeep_values1, average_paio_values1 = zip(*average_paio_per_distance1)
pkeep_values2, average_paio_values2 = zip(*average_paio_per_distance2)

# Plot PAoI as a function of Pkeep for both datasets
plt.plot(pkeep_values1, average_paio_values1, marker='o', linestyle='-', label='RC = [5;15]')
plt.plot(pkeep_values2, average_paio_values2, marker='x', linestyle='-', label='RC = 1')

SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE, family='Times New Roman')          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.grid()
plt.rcParams['font.family'] = 'Times New Roman'
plt.ylim(0, 0.01)
# Add labels and title
plt.xlabel('Pkeep')
plt.ylabel('Average PLR')
# Set y-axis limits

plt.title('Average PLR as a function of Pkeep. Distance =<' + str(distance))

# Add legend
plt.legend()

plt.savefig('meanPLR_vs_Pkeep_RC1vsRC515_Distance' + str(distance)+'.eps')
plt.savefig('meanPLR_vs_Pkeep_RC1vsRC515_Distance' + str(distance)+'.png')
# Show the plot
plt.show()