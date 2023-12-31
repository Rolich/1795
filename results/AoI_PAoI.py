import csv
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict


start_time = time.time()

# Specify the file path
base_path = "Periodic_Dynamic0_avgRRI0_VariableSize0_ReEval0_200_PDB0_867"

# Specify the fields you want to extract
fields = ['rxTime', 'packetID', 'TxDistance', 'txID', 'rxID', 'decoded', 'lossType']

regions_list = list(range(18)) # Array with indexes of regions
print(regions_list)

def calculate_pdr_and_average(simulation_num, packet_total, packet_decodedorlost, distance_region_index, regions_list, pkeep):
    average_pdr_matrix = []

    # Calculate PDR_matrix
    for key in packet_total:
        rxID, txID = key
        if key not in PDR_matrix:
            PDR_matrix[key] = 0

        if key in packet_decodedorlost:
            PDR_matrix[key] = packet_decodedorlost[key] / packet_total[key]
        

    # Calculate average PDR for each distance region
    for region_value in regions_list:
        region_sum = 0
        region_counter = 0

        for key, value in PDR_matrix.items():
            rxID, txID = key
            distance_region = distance_region_index[key]

            if rxID != txID and distance_region == region_value:
                region_sum += value
                region_counter += 1

        if region_counter > 0:
            average_pdr = region_sum / region_counter
        else:
            average_pdr = -1

        average_pdr_matrix.append([simulation_num, (region_value * 50) + 25, average_pdr, pkeep, region_weights[region_value]])

    output_path = 'PDR_matrix_RC515_weight.txt'
    with open(output_path, 'a') as file:
        np.savetxt(file, average_pdr_matrix, delimiter=',', fmt='%.6f')

    return np.array(average_pdr_matrix)

def calculate_clr_and_plr(simulation_num, packet_total, packet_collided, packet_prop_loss, distance_region_index, regions_list, pkeep):
    average_clr_matrix = []
    average_plr_matrix = []

    # Calculate CLR_PLR_matrix
    for key in packet_total:
        rxID, txID = key
        if key not in CLR_matrix:
            CLR_matrix[key] = 0

        if key in packet_collided:
            CLR_matrix[key] = packet_collided[key] / packet_total[key]

        if key not in PLR_matrix:
            PLR_matrix[key] = 0

        if key in packet_prop_loss:
            PLR_matrix[key] = packet_prop_loss[key] / packet_total[key]
        

    # Calculate average CLR for each distance region
    for region_value in regions_list:
        region_sum = 0
        region_counter = 0

        for key, value in CLR_matrix.items():
            rxID, txID = key
            distance_region = distance_region_index[key]

            if rxID != txID and distance_region == region_value:
                region_sum += value
                region_counter += 1

        if region_counter > 0:
            average_clr = region_sum / region_counter
        else:
            average_clr = -1

        average_clr_matrix.append([simulation_num, (region_value * 50) + 25, average_clr, pkeep, region_weights[region_value]])
    
    output_path = 'CLR_matrix_RC515_weight.txt'
    with open(output_path, 'a') as file:
        np.savetxt(file, average_clr_matrix, delimiter=',', fmt='%.6f')

    # Calculate average PLR for each distance region
    for region_value in regions_list:
        region_sum = 0
        region_counter = 0

        for key, value in PLR_matrix.items():
            rxID, txID = key
            distance_region = distance_region_index[key]

            if rxID != txID and distance_region == region_value:
                region_sum += value
                region_counter += 1

        if region_counter > 0:
            average_plr = region_sum / region_counter
        else:
            average_plr = -1

        average_plr_matrix.append([simulation_num, (region_value * 50) + 25, average_plr, pkeep, region_weights[region_value]])

    output_path = 'PLR_matrix_RC515_weight.txt'
    with open(output_path, 'a') as file:
        np.savetxt(file, average_plr_matrix, delimiter=',', fmt='%.6f')

# Function to calculate Packet Inter-Reception (PIR) for each transmitter-receiver pair
def calculate_pir(rxTime, txID_dec, rxID_dec, pir_dict):
    pair_key = (txID_dec, rxID_dec)

    rx_times = pir_dict[pair_key]['rx_times']
    pir_values = pir_dict[pair_key]['pir_values']
    pir_squared_values = pir_dict[pair_key]['pir_squared_values']

    rx_times.append(rxTime)

    # Calculate PIR for each neighboring pair on-the-fly
    if len(rx_times) > 1:
        pir = rx_times[-1] - rx_times[-2]
        pir_values.append(pir)
        pir_squared_values.append(pir * pir)



def calculate_average_aoi(simulation_num, pir_dict, regions_list, pkeep):
    average_aoi_matrix = []
    average_paoi_matrix = []
    pair_aoi_matrix = {}
    pair_paoi_matrix = {}

    for pair_key, data in pir_dict.items():
            txID_dec, rxID_dec = pair_key
            pir_squared_values = data['pir_squared_values']
            pir_values = data['pir_values']
            
            if pir_squared_values and len(pir_values) >= 10 and rxID_dec != txID_dec:
                mean_pir_squared = np.mean(pir_squared_values)
                mean_pir = np.mean(pir_values)
                pair_paoi_matrix [pair_key] = mean_pir
                pair_aoi_matrix [pair_key] = mean_pir_squared / (2 * mean_pir)

    for region_value in regions_list:
        mean_aoi = 0
        mean_paoi = 0
        aoi_sum = 0
        counter = 0
        paoi_sum = 0
        
        for pair_key, data in pair_aoi_matrix.items():
            txID_dec, rxID_dec = pair_key
            distance_region = AoI_distance_region_index.get(pair_key, None)

            if distance_region == region_value and rxID_dec != txID_dec:
                aoi_sum += pair_aoi_matrix [pair_key]
                paoi_sum += pair_paoi_matrix [pair_key]
                counter += 1
        
        if counter > 0:
            mean_aoi = aoi_sum / counter
            mean_paoi = paoi_sum / counter
        
        if paoi_sum == 0:
            mean_aoi = -1
            mean_paoi = -1

        average_aoi_matrix.append([simulation_num, (region_value * 50) + 25, mean_aoi, pkeep, region_weights[region_value]])
        average_paoi_matrix.append([simulation_num, (region_value * 50) + 25, mean_paoi, pkeep, region_weights[region_value]])              

    output_path = 'AoI_matrix_final_RC515_weight.txt'
    with open(output_path, 'a') as file:
        np.savetxt(file, average_aoi_matrix, delimiter=',', fmt='%.6f')

    output_path = 'PAoI_matrix_final_RC515_weight.txt'
    with open(output_path, 'a') as file:
        np.savetxt(file, average_paoi_matrix, delimiter=',', fmt='%.6f')


def process_log_file(file_path, packet_total, packet_decoded, packet_collision_loss, packet_prop_loss, distance_region_index):
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            txID = int(values[7])
            rxID = int(values[8])
            distance_pair = float(values[6])
            
            for i, border in enumerate(border_values):
                if distance_pair <= border:
                    region_value = i
                    current_distance_region_index = i
                    break

            distance_region_index[(rxID, txID)] = current_distance_region_index

            if (rxID, txID) not in packet_total:
                packet_total[(rxID, txID)] = 0
            packet_total[(rxID, txID)] += 1

            if int(values[9]) == 1:
                if (rxID, txID) not in packet_decoded:
                    packet_decoded[(rxID, txID)] = 0

                packet_decoded[(rxID, txID)] += 1

                rxTime = float(values[0])
                txID_dec = int(values[7])
                rxID_dec = int(values[8])
                distance [(rxID_dec, txID_dec)] = float(values[6])
                calculate_pir(rxTime, txID_dec, rxID_dec, pir_dict)
            elif int(values[10]) == 2 or int(values[10]) == 0:
                if (rxID, txID) not in packet_prop_loss:
                    packet_prop_loss[(rxID, txID)] = 0

                packet_prop_loss[(rxID, txID)] += 1
            elif int(values[10]) == 3:
                if (rxID, txID) not in packet_collision_loss:
                    packet_collision_loss[(rxID, txID)] = 0

                packet_collision_loss[(rxID, txID)] += 1


# MAIN
start_simulation = 1000 #number of simulation give infomation about pkeep. If simulation is 1000, pkeep is 0; 1001, pkeep is 0.1 etc. if 1099 pkeep = 0.99
end_simulation = 1000
p_keep = 0 

pir_dict = {}  # Dictionary to store PIR data


for simulation_num in range(start_simulation, end_simulation + 1):
    file_path = base_path + f"_{simulation_num:d}/ReceivedLog.txt"
    PDR_matrix = {}  # Matrix of PDR for each pair
    CLR_matrix = {}  # Matrix of CLR for each pair
    PLR_matrix = {}  # Matrix of PLR for each pair
    packet_total = {}  # Dictionary to store total packet counts for each (rxID, txID) pair
    packet_decoded = {}  # Dictionary to store decoded packet counts for each (rxID, txID) pair
    packet_collision_loss = {}  # Dictionary to store lost by propagation packet counts for each (rxID, txID) pair
    packet_prop_loss = {}  # Dictionary to store lost by collision packet counts for each (rxID, txID) pair
    distance_region_index = {}  # Matrix to store indexes of regions
    AoI_distance_region_index = {}  # Matrix to store indexes of regions for AoI calculation
    distance = {} # Distance between pairs
    region_weights = {}
    border_values = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]

    pir_dict = defaultdict(lambda: {'rx_times': [], 'pir_values': [], 'pir_squared_values': []})

    if os.path.exists(file_path):
        process_log_file(file_path, packet_total, packet_decoded, packet_collision_loss, packet_prop_loss, distance_region_index)

        # Create a dictionary to store counts of unique pairs in each distance region
        pair_counts_by_region = defaultdict(int)
        

        # Initialize the counts for each region
        pair_counts_by_region = {i: 0 for i in range(len(border_values))}

        # Iterate over the distance dictionary
        for pair_key, distance_data in distance.items():
            rxID_dec, txID_dec = pair_key
            distance_value = distance_data
              
            # Check if the distance is within a specific border
            for i, border in enumerate(border_values):
                if distance_value <= border:
                    region_value = i
                    AoI_distance_region_index[(rxID_dec, txID_dec)] = i
                    pair_counts_by_region[region_value] += 1
                    break

        # Calculate the total number of unique pairs
        total_unique_pairs = sum(pair_counts_by_region.values())

        # Print the counts in each region
        for region_value, count in pair_counts_by_region.items():
            print(f"Region {region_value}: {count} pairs")

        # Print the overall count
        print(f"Overall count: {total_unique_pairs}")

        # Create a structure to hold the weights
        region_weights = {region_value: count / total_unique_pairs for region_value, count in pair_counts_by_region.items()}

        calculate_pdr_and_average(simulation_num, packet_total, packet_decoded, distance_region_index, regions_list, p_keep)
        calculate_clr_and_plr(simulation_num, packet_total, packet_collision_loss, packet_prop_loss, distance_region_index, regions_list, p_keep)
        calculate_average_aoi(simulation_num, pir_dict, regions_list, p_keep)

end_time = time.time()
print(f"Done successfully! Script running time: {end_time - start_time} seconds.")
