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

int main(int argc, char const *argv[])
{
	pid_t pid1, pid2, pid3, pid4;
	int running1, running2, running3, running4;

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

    // Array to store workload for each process
    int workloads[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
    pid_t pids[] = {pid1, pid2, pid3, pid4};
    int *runnings[] = {&running1, &running2, &running3, &running4};

    // Sort processes based on workload (bubble sort for simplicity)
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3 - i; j++) {
            if (workloads[j] > workloads[j + 1]) {
                // Swap workloads
                int temp_workload = workloads[j];
                workloads[j] = workloads[j + 1];
                workloads[j + 1] = temp_workload;

                // Swap PIDs
                pid_t temp_pid = pids[j];
                pids[j] = pids[j + 1];
                pids[j + 1] = temp_pid;

                // Swap running pointers
                int *temp_running = runnings[j];
                runnings[j] = runnings[j + 1];
                runnings[j + 1] = temp_running;
            }
        }
    }

    // Execute processes in sorted order
    for (int i = 0; i < 4; i++) {
        while (*runnings[i] > 0) {
            kill(pids[i], SIGCONT);
            usleep(1000);  // Let the process run for a short time
            kill(pids[i], SIGSTOP);
            waitpid(pids[i], runnings[i], WNOHANG);
        }
        printf("Process with PID %d (workload: %d) has completed\n", pids[i], workloads[i]);
    }
	
	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/

	return 0;
}