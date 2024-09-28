#!/bin/bash

# Compile the program
gcc -o sum_multitasking_1 sum_multitasking_1.c

# Arrays of N and num_processes values
N_values=(100000000 1000000000 10000000000)
process_values=(2 4 8)

# Output file
output_file="sum_multitasking_1_results.txt"

# Clear the output file if it exists
> "$output_file"

# Run tests
for N in "${N_values[@]}"; do
    for num_processes in "${process_values[@]}"; do
        echo "Testing with N = $N and num_processes = $num_processes" | tee -a "$output_file"
        
        # Run the program with time command and append output to file
        { time ./sum_multitasking_1 $N $num_processes; } 2>&1 | tee -a "$output_file"
        
        echo "--------------------" | tee -a "$output_file"
    done
done

echo "Test results have been written to $output_file"