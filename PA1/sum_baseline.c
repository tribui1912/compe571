#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <N>\n", argv[0]);
        return 1;
    }

    unsigned long long N = strtoull(argv[1], NULL, 10);
    unsigned long long sum = 0;
    for (unsigned long long i = 0; i < N; i++) {
        sum += i;
    }

    printf("The sum of integers from 0 to %llu (exclusive) is: %llu\n", N, sum);
    return 0;
}
