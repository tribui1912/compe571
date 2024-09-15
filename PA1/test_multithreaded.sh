#!/bin/bash

# Compile the C program
gcc -o sum_multithreaded.o sum_multithreaded.c -pthread

# Test values and expected results
declare -A expected_results=(
    [100000000]="4999999950000000"
    [1000000000]="499999999500000000"
    [10000000000]="49999999995000000000"
)

N_values=(100000000 1000000000 10000000000)
thread_counts=(2 4 8)

# Output files
results_file="sum_multithreaded_results.txt"
time_file="sum_multithreaded_times.txt"

# Clear the output files if they exist
> "$results_file"
> "$time_file"

# Run tests
for N in "${N_values[@]}"
do
    for threads in "${thread_counts[@]}"
    do
        echo "Testing with N = $N and threads = $threads" >> "$results_file"
        
        # Run the program, capture its output and time
        result=$(./sum_multithreaded.o $N $threads)
        time_output=$( { time ./sum_multithreaded.o $N $threads ; } 2>&1 )
        
        if [[ "$result" == "${expected_results[$N]}" ]]; then
            echo -e "Test passed \u2713"  # Unicode check mark
            echo "Test passed" >> "$results_file"
        else
            echo "Test failed. Expected: ${expected_results[$N]}, Got: $result"
            echo "Test failed. Expected: ${expected_results[$N]}, Got: $result" >> "$results_file"
        fi
        
        # Extract real time and save to time file
        real_time=$(echo "$time_output" | grep real | awk '{print $2}')
        echo "N = $N, Threads = $threads, Time = $real_time" >> "$time_file"
        
        echo "------------------------" >> "$results_file"
    done
done

echo "Test results have been written to $results_file"
echo "Execution times have been written to $time_file"
