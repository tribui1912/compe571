#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

/// Create struct for passing arguement to each thread 
typedef struct {
    long long start, end;
    long long partial_sum;
} ThreadArgs;

/// Sum using for each thread
void* sum_range(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;
    args->partial_sum = 0;
    for (long long i = args->start; i < args->end; i++) {
        args->partial_sum += i;
    }
    return NULL;
}

/// Main function
int main(int argc, char *argv[]) {
    /// Checking commmand-line arguement 
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <N> <num_threads>\n", argv[0]);
        return 1;
    }
    
    /// Parsing arguement 
    long long N = atoll(argv[1]);
    int num_threads = atoi(argv[2]);
    
    /// Preparing thread and arguement arrays
    pthread_t threads[num_threads];
    ThreadArgs args[num_threads];
    long long chunk_size = N / num_threads;
    
    /// Loop to create threads and assigning range to sum for each thread 
    for (int i = 0; i < num_threads; i++) {
        args[i].start = i * chunk_size;
        args[i].end = (i == num_threads - 1) ? N : (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, sum_range, &args[i]);
    }
    
    /// Joining thread and adding up the sum results
    long long total_sum = 0;
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
        total_sum += args[i].partial_sum;
    }

    /// Remove for checking the total of sum
    /// printf("Sum: %lld\n", total_sum);
    return 0;
}

