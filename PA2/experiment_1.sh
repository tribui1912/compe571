#!/bin/bash

PROGRAM_PATH="./sample.o"
QUANTA=(1000 2500 5000 7500 10000 15000 20000 50000 100000)
RUNS_PER_QUANTUM=5
OUTPUT_FILE="experiment_1.txt"
COOLDOWN_TIME=5  # Cooldown time in seconds

# Clear the output file if it exists
> $OUTPUT_FILE

for quantum in "${QUANTA[@]}"; do
    echo "Quantum: $quantum" >> $OUTPUT_FILE
    for ((i=1; i<=RUNS_PER_QUANTUM; i++)); do
        # Run the program with highest priority
        sudo nice -20 $PROGRAM_PATH $quantum | grep "Average response time:" >> $OUTPUT_FILE
        
        # Cooldown period
        sleep $COOLDOWN_TIME
    done
    echo "" >> $OUTPUT_FILE
done

echo "Finished running experiments, now processing results"

python3 experiment_1.py




