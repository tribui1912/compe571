#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <start> <end>\n", argv[0]);
        return 1;
    }

    unsigned long long start = strtoull(argv[1], NULL, 10);
    unsigned long long end = strtoull(argv[2], NULL, 10);
    unsigned long long sum = 0;

    for (unsigned long long i = start; i < end; i++) {
        sum += i;
    }

    printf("%llu\n", sum);
    return 0;
}
