#!/bin/bash

# Path to your simulation executable
SIM_EXECUTABLE="./waf"

# Simulation parameters
SIM_PARAMETERS="--Vehicles=800 --noIBE --ChannelBW=10 --Periodic --simTime=30 --SubChannel=20 --Numerology=0 --ueTxPower=20"

# Initialize Pkeep to 0
Pkeep=0

# Loop until Pkeep reaches 0.9
while (( $(echo "$Pkeep <= 0.9" | bc -l) )); do
    # Run the simulation with the current Pkeep value
    $SIM_EXECUTABLE --run "scratch/HIGHWAY --Pkeep=$Pkeep $SIM_PARAMETERS"
    
    # Increment Pkeep by 0.1
    Pkeep=$(echo "$Pkeep + 0.1" | bc -l)
done


