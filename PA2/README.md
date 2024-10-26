### Experiment 1: Finding the best quantum value for Round Robin Scheduling

int main(int argc, char const *argv[])
{
    // ... existing code ...

    int quantum = QUANTUM1;  // Default value
    if (argc > 1) {
        quantum = atoi(argv[1]);
    }

    struct Process processes[] = {
        {pid1, &running1, "WORKLOAD1", quantum, {0}, 0, 0},
        {pid2, &running2, "WORKLOAD2", quantum, {0}, 0, 0},
        {pid3, &running3, "WORKLOAD3", quantum, {0}, 0, 0},
        {pid4, &running4, "WORKLOAD4", quantum, {0}, 0, 0}
    };

    // ... rest of the code ...
}

by changing the main function to take in a quantum value as a command line argument, we can test the performance of the program with different quantum values.

### Experiment 2: Best quantum value for MLFQ



