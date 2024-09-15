#include <stdio.h>
#include <stdlib.h>

/// Define uint128_t since some compilers may not have it (caused problem in my case)
typedef unsigned __int128 uint128_t;

/// Function to print uint128_t
void print_uint128(uint128_t n) {
    char buffer[40];
    int i = 0;
    if (n == 0) {
        putchar('0');
        return;
    }
    while (n > 0) {
        buffer[i++] = '0' + n % 10;
        n /= 10;
    }
    while (i--) {
        putchar(buffer[i]);
    }
    putchar('\n');
}

/// Main function (was similar to previous version but used uint128_t instead of long long)
int main(int argc, char *argv[]) {
    uint128_t N = strtoull(argv[1], NULL, 10);
    uint128_t sum = 0;

    for (uint128_t i = 0; i < N; ++i) {
        sum += i;
    }

    print_uint128(sum);
    return 0;
}
