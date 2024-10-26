#!/bin/bash

# Function to compile and run a program with highest priority
compile_and_run() {
    program=$1
    output_file=$2

    echo "Running $program..." >> "$output_file"

    # Compile the program
    gcc -o "${program}.o" "${program}.c"

    # Run the program with highest priority and extract context switch information
    sudo nice -20 ./"${program}.o" | grep -E "Total context switch time|Number of context switches|Average context switch time" >> "$output_file"

    # Add a newline for readability
    echo "" >> "$output_file"

    # Clean up
    rm "${program}.o"
}

# Run the entire process 6 times
for i in {0..5}
do
    # Output file for context switch information
    context_switch_file="context_switch_$i.txt"

    # Clear the context switch file if it exists
    > "$context_switch_file"

    echo "Run $i" >> "$context_switch_file"
    echo "======" >> "$context_switch_file"

    # Compile and run programs in order with highest priority
    sudo bash -c "
        $(declare -f compile_and_run)
        compile_and_run sample_program '$context_switch_file'
        compile_and_run SJF_implementation '$context_switch_file'
        compile_and_run FCFS_implementation '$context_switch_file'
        compile_and_run MLFQ_implementation '$context_switch_file'
    "

    echo "Run $i completed. Results saved to $context_switch_file"
    echo ""
done

echo "All runs completed. Results saved to context_switch_[0-5].txt files."
