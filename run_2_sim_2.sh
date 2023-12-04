#!/bin/bash

# Path to your simulation executable
SIM_EXECUTABLE="./waf"

# Simulation parameters
SIM_PARAMETERS="--Vehicles=2 --noIBE --ChannelBW=10 --Periodic --simTime=250 --SubChannel=25 --Numerology=0 --ueTxPower=23"

# Loop through run numbers from 1 to 1000
for ((runNo=999799; runNo<=999799; runNo++)); do
    # Run the simulation with the current run number
    $SIM_EXECUTABLE --run "scratch/HIGHWAY --runNo=$runNo $SIM_PARAMETERS"
done
