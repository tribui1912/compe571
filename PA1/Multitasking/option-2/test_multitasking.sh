#!/bin/bash

# Compile the C programs
gcc -o sum_helper.o sum_helper.c
gcc -o sum_multitasking.o sum_multitasking.c

# Test values
N_values=(100000000 1000000000 10000000000)
process_counts=(2 4 8)

# Output file
output_file="sum_multitasking_results.txt"

# Clear the output file if it exists
> "$output_file"

# Run tests
for N in "${N_values[@]}"
do
    for processes in "${process_counts[@]}"
    do
        echo "Testing with N = $N and processes = $processes" >> "$output_file"
        { time ./sum_multitasking.o $N $processes ; } 2>> "$output_file"
        echo "------------------------" >> "$output_file"
    done
done

echo "Test results have been written to $output_file"
