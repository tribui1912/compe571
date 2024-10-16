#!/bin/bash

# Output file for response times
response_times_file="response_times.txt"

# Clear the response times file if it exists
> $response_times_file

# Function to compile and run a program
compile_and_run() {
    program=$1
    output_file=$2

    echo "Running $program..." >> $response_times_file

    # Compile the program
    gcc -o $program $program.c

    # Run the program and extract response times
    ./$program | grep "Response time" >> $response_times_file

    # Add a newline for readability
    echo "" >> $response_times_file

    # Clean up
    rm $program
}

# Compile and run programs in order
compile_and_run sample_program sample.o
compile_and_run SJF_implementation SJF.o
compile_and_run FCFS_implementation FCFS.o
compile_and_run MLFQ_implementation MLFQ.o

echo "All programs have been compiled, run, and response times saved to $response_times_file"