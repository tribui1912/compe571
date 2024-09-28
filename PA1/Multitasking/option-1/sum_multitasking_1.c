#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <N> <num_processes>\n", argv[0]);
        return 1;
    }

    unsigned long long N = strtoull(argv[1], NULL, 10);
    int num_processes = atoi(argv[2]);

    if (num_processes <= 0) {
        fprintf(stderr, "Number of processes must be positive\n");
        return 1;
    }

    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }

    unsigned long long sum = 0;
    pid_t pid;

    for (int i = 0; i < num_processes; i++) {
        pid = fork();

        if (pid == -1) {
            perror("fork");
            exit(1);
        } else if (pid == 0) {
            // Child process
            close(pipefd[0]);
            unsigned long long start = (N * i) / num_processes;
            unsigned long long end = (N * (i + 1)) / num_processes;
            unsigned long long partial_sum = 0;

            for (unsigned long long j = start; j < end; j++) {
                partial_sum += j;
            }

            write(pipefd[1], &partial_sum, sizeof(partial_sum));
            close(pipefd[1]);
            exit(0);
        }
    }

    // Parent process
    close(pipefd[1]);
    unsigned long long partial_sum;

    for (int i = 0; i < num_processes; i++) {
        read(pipefd[0], &partial_sum, sizeof(partial_sum));
        sum += partial_sum;
        wait(NULL);
    }

    close(pipefd[0]);

    printf("The sum of integers from 0 to %llu (exclusive) is: %llu\n", N, sum);
    return 0;
}