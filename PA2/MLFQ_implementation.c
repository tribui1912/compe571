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
    int in_first_queue;
};

int main(int argc, char const *argv[])
{
	pid_t pid1, pid2, pid3, pid4;
	int running1 = 1, running2 = 1, running3 = 1, running4 = 1;

	pid1 = fork();

	if (pid1 == 0){

		myfunction(WORKLOAD1);

		exit(0);
	}
	kill(pid1, SIGSTOP);

	pid2 = fork();

	if (pid2 == 0){

		myfunction(WORKLOAD2);

		exit(0);
	}
	kill(pid2, SIGSTOP);

	pid3 = fork();

	if (pid3 == 0){

		myfunction(WORKLOAD3);

		exit(0);
	}
	kill(pid3, SIGSTOP);

	pid4 = fork();

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
        {pid1, &running1, "WORKLOAD1", 1},
        {pid2, &running2, "WORKLOAD2", 1},
        {pid3, &running3, "WORKLOAD3", 1},
        {pid4, &running4, "WORKLOAD4", 1}
    };
    int num_processes = sizeof(processes) / sizeof(processes[0]);
    int processes_in_first_queue = num_processes;

    while (processes_in_first_queue > 0 || 
           (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0)) {
        
        // First level queue (Round Robin)
        for (int i = 0; i < num_processes; i++) {
            if (processes[i].in_first_queue && *(processes[i].running) > 0) {
                printf("Running process %s in first queue\n", processes[i].name);
                kill(processes[i].pid, SIGCONT);
                usleep(QUANTUM1);
                kill(processes[i].pid, SIGSTOP);
                
                waitpid(processes[i].pid, processes[i].running, WNOHANG);
                
                if (*(processes[i].running) > 0) {
                    // Process didn't finish, move to second queue
                    processes[i].in_first_queue = 0;
                    processes_in_first_queue--;
                    printf("Moving process %s to second queue\n", processes[i].name);
                } else {
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
                waitpid(processes[i].pid, processes[i].running, 0);  // Wait for process to complete
                printf("Process %s completed in second queue\n", processes[i].name);
            }
        }
    }
	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/

	return 0;
}