#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

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
    }
    return NULL;
}

int main(int argc, char *argv[]) {
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
    return 0;
}