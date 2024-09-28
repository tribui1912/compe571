#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

<<<<<<< HEAD
typedef struct {
    unsigned long long start;
    unsigned long long end;
    unsigned long long partial_sum;
} ThreadData;

void *calculate_partial_sum(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    data->partial_sum = 0;
    for (unsigned long long i = data->start; i < data->end; i++) {
        data->partial_sum += i;
=======
// Define uint128_t since some compilers may not have it
// 128-bit unsigned integer type
typedef unsigned __int128 uint128_t;

// Structure to pass arguments to the thread function
// Used to pass multiple parameters to our thread function
typedef struct {
    uint128_t start;     // Starting number for this thread's range
    uint128_t end;       // Ending number (exclusive) for this thread's range
    uint128_t partial_sum;  // Partial sum for this thread
} ThreadArgs;

// Function to print uint128_t
// Printf doesn't support uint128_t directly
void print_uint128(uint128_t n) {
    char buffer[40];  // Buffer to store digits (more than enough for 128-bit numbers)
    int i = 0;
    if (n == 0) {
        putchar('0');
        return;
    }
    // Extract digits in reverse order
    while (n > 0) {
        buffer[i++] = '0' + n % 10;  // Get least significant digit
        n /= 10;  // Move to next digit
    }
    // Print digits in correct order
    while (i--) {
        putchar(buffer[i]);
    }
    putchar('\n');
}

// Thread function to calculate partial sum
// Function executed by each thread
void* calculate_partial_sum(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;
    args->partial_sum = 0;
    // Calculate sum for the assigned range
    for (uint128_t i = args->start; i < args->end; ++i) {
        args->partial_sum += i;
>>>>>>> refs/remotes/origin/main
    }
    return NULL;
}

int main(int argc, char *argv[]) {
<<<<<<< HEAD
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <N> <num_threads>\n", argv[0]);
        return 1;
    }

    unsigned long long N = strtoull(argv[1], NULL, 10);
    int num_threads = atoi(argv[2]);

    pthread_t *threads = malloc(num_threads * sizeof(pthread_t));
    ThreadData *thread_data = malloc(num_threads * sizeof(ThreadData));
    unsigned long long chunk_size = N / num_threads;

    for (int i = 0; i < num_threads; i++) {
        thread_data[i].start = i * chunk_size;
        thread_data[i].end = (i == num_threads - 1) ? N : (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, calculate_partial_sum, &thread_data[i]);
    }

    unsigned long long total_sum = 0;
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
        total_sum += thread_data[i].partial_sum;
    }

    printf("Sum to %llu using %d threads is: %llu\n", N, num_threads, total_sum);

    free(threads);
    free(thread_data);
=======
    // Parse command-line arguments
    uint128_t N = strtoull(argv[1], NULL, 10);  // Total number N
    int num_threads = atoi(argv[2]);  // Number of threads

    // Declare arrays for thread handles and arguments
    pthread_t threads[num_threads];
    ThreadArgs thread_args[num_threads];

    // Calculate the size of work each thread should handle
    uint128_t chunk_size = N / num_threads;
    uint128_t total_sum = 0;

    // Create threads
    for (int i = 0; i < num_threads; ++i) {
        // Set the range for this thread
        thread_args[i].start = i * chunk_size;
        // For the last thread, make sure we go up to N
        thread_args[i].end = (i == num_threads - 1) ? N : (i + 1) * chunk_size;
        // Create the thread and pass it its arguments
        pthread_create(&threads[i], NULL, calculate_partial_sum, &thread_args[i]);
    }

    // Join threads and sum up partial results
    for (int i = 0; i < num_threads; ++i) {
        // Wait for this thread to finish
        pthread_join(threads[i], NULL);
        total_sum += thread_args[i].partial_sum;
    }

    // Print the final result
    // printf("Sum: ");
    print_uint128(total_sum);

>>>>>>> refs/remotes/origin/main
    return 0;
}