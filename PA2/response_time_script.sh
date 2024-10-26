#!/bin/bash

# Function to compile and run a program with highest priority
compile_and_run() {
    program=$1
    output_file=$2

    echo "Running $program..." >> "$output_file"

    # Compile the program
    gcc -o "${program}.o" "${program}.c"

    # Run the program with highest priority and extract response times
    sudo nice -20 ./"${program}.o" | grep "Response time" | sort >> "$output_file"

    # Add a newline for readability
    echo "" >> "$output_file"

    # Clean up
    rm "${program}.o"
}

# Run the entire process 6 times
for i in {0..5}
do
    # Output file for response times
    response_times_file="response_times_$i.txt"

    # Clear the response times file if it exists
    > "$response_times_file"

    echo "Run $i" >> "$response_times_file"
    echo "======" >> "$response_times_file"

    # Compile and run programs in order with highest priority
    sudo bash -c "
        $(declare -f compile_and_run)
        compile_and_run sample_program '$response_times_file'
        compile_and_run SJF_implementation '$response_times_file'
        compile_and_run FCFS_implementation '$response_times_file'
        compile_and_run MLFQ_implementation '$response_times_file'
    "

    echo "Run $i completed. Results saved to $response_times_file"
    echo ""
done

echo "All runs completed. Results saved to response_times_[0-5].txt files."
