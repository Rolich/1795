SIM_EXECUTABLE="./waf"

# Simulation parameters
SIM_PARAMETERS="--Vehicles=2 --noIBE --ChannelBW=10 --Periodic --simTime=250 --SubChannel=12 --Numerology=0 --ueTxPower=13"

# Loop through run numbers from 1 to 1000
for ((runNo=10000; runNo<=10250; runNo++)); do
    # Run the simulation with the current run number
    $SIM_EXECUTABLE --run "scratch/HIGHWAY --runNo=$runNo $SIM_PARAMETERS"
done