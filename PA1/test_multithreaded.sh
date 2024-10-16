#!/bin/bash

# Compile the C program
gcc -o sum_multithreaded.o sum_multithreaded.c -pthread

# Test values
N_values=(100000000 1000000000 10000000000)
thread_counts=(2 4 8)
c
# Output file
output_file="sum_multithreaded_results.txt"

# Clear the output file if it exists
> "$output_file"

# Run tests
for N in "${N_values[@]}"
do
    for threads in "${thread_counts[@]}"
    do
        echo "Testing with N = $N and threads = $threads" >> "$output_file"
        { time ./sum_multithreaded.o $N $threads ; } 2>> "$output_file"
        echo "------------------------" >> "$output_file"
    done
done

echo "Test results have been written to $output_file"
