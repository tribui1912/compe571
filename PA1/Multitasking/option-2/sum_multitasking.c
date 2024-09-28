#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_PROCESSES 64

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <N> <num_processes>\n", argv[0]);
        return 1;
    }

    unsigned long long N = strtoull(argv[1], NULL, 10);
    int num_processes = atoi(argv[2]);

    if (num_processes <= 0 || num_processes > N) {
        fprintf(stderr, "Invalid number of processes. Must be between 1 and N.\n");
        return 1;
    }

    unsigned long long total_sum = 0;
    FILE *pipes[MAX_PROCESSES];
    
    // Start all processes concurrently
    for (int i = 0; i < num_processes; i++) {
        unsigned long long start = (N * i) / num_processes;
        unsigned long long end = (N * (i + 1)) / num_processes;

        char command[256];
        snprintf(command, sizeof(command), 
                 "./sum_helper.o %llu %llu", start, end);

        pipes[i] = popen(command, "r");
        if (pipes[i] == NULL) {
            perror("popen");
            exit(1);
        }
    }

    // Collect results from all processes
    for (int i = 0; i < num_processes; i++) {
        unsigned long long partial_result;
        if (fscanf(pipes[i], "%llu", &partial_result) != 1) {
            fprintf(stderr, "Error reading from pipe %d\n", i);
            exit(1);
        }

        total_sum += partial_result;
        pclose(pipes[i]);
    }

    printf("The sum of integers from 0 to %llu (exclusive) is: %llu\n", N, total_sum);
    return 0;
}