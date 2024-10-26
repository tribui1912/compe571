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

// #define WORKLOAD1 100000
// #define WORKLOAD2 100000
// #define WORKLOAD3 100000
// #define WORKLOAD4 100000

#define WORKLOAD1 100000
#define WORKLOAD2 50000
#define WORKLOAD3 25000
#define WORKLOAD4 10000

#define QUANTUM1 75000
#define QUANTUM2 75000
#define QUANTUM3 75000
#define QUANTUM4 75000

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
    int in_first_queue;
    struct timeval start_time;
    struct timeval completion_time;
    int has_completed;
    int has_started;  // Add this line
    long response_time;  // Add this line
};

long get_elapsed_time(struct timeval start, struct timeval end) {
    return (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);
}

struct TimingInfo {
    struct timeval start;
    struct timeval end;
    long total_time;
    int switch_count;
};

int main(int argc, char const *argv[])
{
	pid_t pid1, pid2, pid3, pid4;
	int running1 = 1, running2 = 1, running3 = 1, running4 = 1;
	struct timeval current_time;

	// Use defined QUANTUM if no argument is provided, otherwise use the argument
	int quantum = QUANTUM1;  // Default to the defined QUANTUM1
	if (argc > 1) {
		quantum = atoi(argv[1]);
	}

	pid1 = fork();
	gettimeofday(&current_time, NULL);
	if (pid1 == 0){
		myfunction(WORKLOAD1);
		exit(0);
	}
	kill(pid1, SIGSTOP);

	pid2 = fork();
	gettimeofday(&current_time, NULL);
	if (pid2 == 0){
		myfunction(WORKLOAD2);
		exit(0);
	}
	kill(pid2, SIGSTOP);

	pid3 = fork();
	gettimeofday(&current_time, NULL);
	if (pid3 == 0){
		myfunction(WORKLOAD3);
		exit(0);
	}
	kill(pid3, SIGSTOP);

	pid4 = fork();
	gettimeofday(&current_time, NULL);
	if (pid4 == 0){
		myfunction(WORKLOAD4);
		exit(0);
	}
	kill(pid4, SIGSTOP);

	/************************************************************************************************ 
		At this point, all  newly-created child processes are stopped, and ready for scheduling.
	*************************************************************************************************/



	/************************************************************************************************
			- Scheduling code starts here
			- Below is a sample schedule. (which scheduling algorithm is this?)
			- For the assignment purposes, you have to replace this part with the other scheduling methods 
			to be implemented.
	************************************************************************************************/

	struct Process processes[] = {
		{pid1, &running1, "WORKLOAD1", 1, {0}, {0}, 0, 0, 0},  // Initialize has_started and response_time
		{pid2, &running2, "WORKLOAD2", 1, {0}, {0}, 0, 0, 0},
		{pid3, &running3, "WORKLOAD3", 1, {0}, {0}, 0, 0, 0},
		{pid4, &running4, "WORKLOAD4", 1, {0}, {0}, 0, 0, 0}
	};
	int num_processes = sizeof(processes) / sizeof(processes[0]);
	int processes_in_first_queue = num_processes;

	struct TimingInfo timing = {.total_time = 0, .switch_count = 0};

	while (processes_in_first_queue > 0 || 
		   (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0)) {
		
		// First level queue (Round Robin)
		for (int i = 0; i < num_processes; i++) {
			if (processes[i].in_first_queue && *(processes[i].running) > 0) {
				if (!processes[i].has_started) {
					gettimeofday(&processes[i].start_time, NULL);
					processes[i].has_started = 1;
				}

				printf("Running process %s in first queue\n", processes[i].name);
				kill(processes[i].pid, SIGCONT);
				gettimeofday(&timing.start, NULL);
				kill(processes[i].pid, SIGSTOP);
				gettimeofday(&timing.end, NULL);
				timing.total_time += get_elapsed_time(timing.start, timing.end);
				timing.switch_count++;
				usleep(quantum);  
				
				waitpid(processes[i].pid, processes[i].running, WNOHANG);
				
				if (*(processes[i].running) > 0) {
					processes[i].in_first_queue = 0;
					processes_in_first_queue--;
					printf("Moving process %s to second queue\n", processes[i].name);
				} else {
					gettimeofday(&processes[i].completion_time, NULL);
					processes[i].has_completed = 1;
					processes[i].response_time = get_elapsed_time(processes[i].start_time, processes[i].completion_time);
					printf("Response time for %s: %ld microseconds\n", processes[i].name, processes[i].response_time);
					printf("Process %s completed in first queue\n", processes[i].name);
					processes_in_first_queue--;
				}
			}
		}
		
		// Second level queue (FCFS)
		for (int i = 0; i < num_processes; i++) {
			if (!processes[i].in_first_queue && *(processes[i].running) > 0) {
				printf("Running process %s in second queue\n", processes[i].name);
				kill(processes[i].pid, SIGCONT);
				gettimeofday(&timing.start, NULL);
				waitpid(processes[i].pid, processes[i].running, 0);
				gettimeofday(&timing.end, NULL);
				timing.total_time += get_elapsed_time(timing.start, timing.end);
				timing.switch_count++;
				if (!processes[i].has_completed) {
					gettimeofday(&processes[i].completion_time, NULL);
					processes[i].has_completed = 1;
					processes[i].response_time = get_elapsed_time(processes[i].start_time, processes[i].completion_time);
					printf("Response time for %s: %ld microseconds\n", processes[i].name, processes[i].response_time);
				}
				printf("Process %s completed in second queue\n", processes[i].name);
			}
		}
	}
	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/

	// Calculate and print average response time
	long total_response_time = 0;
	int completed_processes = 0;
	for (int i = 0; i < num_processes; i++) {
		if (processes[i].has_completed) {
			total_response_time += processes[i].response_time;
			completed_processes++;
		}
	}
	printf("Average response time: %ld microseconds\n", total_response_time / completed_processes);

	printf("Total context switch time: %ld microseconds\n", timing.total_time);
	printf("Number of context switches: %d\n", timing.switch_count);
	printf("Average context switch time: %ld microseconds\n", timing.total_time / timing.switch_count);

	return 0;
}
