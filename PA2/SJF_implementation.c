#include <stdio.h> 
#include <sys/types.h> 
#include <unistd.h>  
#include <stdlib.h>  
#include <sys/wait.h> 
#include <string.h> 
#include <time.h> 
#include <signal.h>
#include <sys/time.h>

/************************************************************************************************ 
		These DEFINE statements represent the workload size of each task and 
		the time quantum values for Round Robin scheduling for each task.
*************************************************************************************************/

#define WORKLOAD1 100000
#define WORKLOAD2 50000
#define WORKLOAD3 25000
#define WORKLOAD4 10000

#define QUANTUM1 1000
#define QUANTUM2 1000
#define QUANTUM3 1000
#define QUANTUM4 1000

/************************************************************************************************ 
					DO NOT CHANGE THE FUNCTION IMPLEMENTATION
*************************************************************************************************/
void myfunction(int param){

	int i = 2;
	int j, k;

	while(i < param){
		k = i; 
		for (j = 2; j <= k; j++)
		{
			if (k % j == 0){
				k = k/j;
				j--;
				if (k == 1){
					break;
				}
			}
		}
		i++;
	}
}
/************************************************************************************************/

struct Process {
    pid_t pid;
    int *running;
    const char *name;
    int workload;
    struct timeval start_time;
    struct timeval completion_time;
    int has_started;
};

long get_elapsed_time(struct timeval start, struct timeval end) {
    return (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
}

int main(int argc, char const *argv[])
{
    pid_t pid1, pid2, pid3, pid4;
    int running1 = 1, running2 = 1, running3 = 1, running4 = 1;
    struct timeval current_time;

    gettimeofday(&current_time, NULL);
    pid1 = fork();
    if (pid1 == 0) {
        myfunction(WORKLOAD1);
        exit(0);
    }
    kill(pid1, SIGSTOP);

    pid2 = fork();
    if (pid2 == 0) {
        myfunction(WORKLOAD2);
        exit(0);
    }
    kill(pid2, SIGSTOP);

    pid3 = fork();
    if (pid3 == 0) {
        myfunction(WORKLOAD3);
        exit(0);
    }
    kill(pid3, SIGSTOP);

    pid4 = fork();
    if (pid4 == 0) {
        myfunction(WORKLOAD4);
        exit(0);
    }
    kill(pid4, SIGSTOP);

    struct Process processes[] = {
        {pid1, &running1, "WORKLOAD1", WORKLOAD1, {0}, {0}, 0},
        {pid2, &running2, "WORKLOAD2", WORKLOAD2, {0}, {0}, 0},
        {pid3, &running3, "WORKLOAD3", WORKLOAD3, {0}, {0}, 0},
        {pid4, &running4, "WORKLOAD4", WORKLOAD4, {0}, {0}, 0}
    };
    int num_processes = sizeof(processes) / sizeof(processes[0]);

    // Sort processes based on workload (bubble sort)
    for (int i = 0; i < num_processes - 1; i++) {
        for (int j = 0; j < num_processes - i - 1; j++) {
            if (processes[j].workload > processes[j + 1].workload) {
                struct Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }

    for (int i = 0; i < num_processes; i++) {
        printf("Starting process %s (workload: %d)\n", processes[i].name, processes[i].workload);
        
        gettimeofday(&processes[i].start_time, NULL);
        
        while (*processes[i].running > 0) {
            kill(processes[i].pid, SIGCONT);
            
            usleep(1000);
            kill(processes[i].pid, SIGSTOP);
            waitpid(processes[i].pid, processes[i].running, WNOHANG);
        }
        
        gettimeofday(&processes[i].completion_time, NULL);
        long turnaround_time = get_elapsed_time(processes[i].start_time, processes[i].completion_time);
        printf("Response time for %s: %ld microseconds\n", processes[i].name, turnaround_time);
        
        printf("Process %s has completed\n", processes[i].name);
    }

    return 0;
}
