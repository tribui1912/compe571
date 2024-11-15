import sys
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class Task:
    name: str
    period: int  # same as deadline
    wcet: dict[int, int]  # frequency -> execution time

@dataclass
class CPUPower:
    frequencies: List[int]  # MHz
    active_power: dict[int, int]  # frequency -> power in mW
    idle_power: int  # mW

def parse_input(filename: str) -> Tuple[List[Task], CPUPower, int]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse first line
    first_line = lines[0].strip().split()
    num_tasks = int(first_line[0])
    total_time = int(first_line[1])
    
    # CPU frequencies in MHz
    frequencies = [1188, 918, 648, 384]
    
    # Parse power values
    active_power = dict(zip(frequencies, map(int, first_line[2:6])))
    idle_power = int(first_line[6])
    cpu_power = CPUPower(frequencies, active_power, idle_power)
    
    # Parse tasks
    tasks = []
    for i in range(num_tasks):
        line = lines[i + 1].strip().split()
        name = line[0]
        period = int(line[1])
        wcet = dict(zip(frequencies, map(int, line[2:])))
        tasks.append(Task(name, period, wcet))
    
    return tasks, cpu_power, total_time

def calculate_energy(power_mw: int, time_s: int) -> float:
    """Calculate energy in Joules given power in mW and time in seconds"""
    return (power_mw * time_s) / 1000.0

class Scheduler:
    def __init__(self, tasks: List[Task], cpu_power: CPUPower, total_time: int):
        self.tasks = tasks
        self.cpu_power = cpu_power
        self.total_time = total_time
        self.schedule = []  # List of (start_time, task, freq, duration, energy)
    
    def get_next_release_times(self, task: Task, completed_jobs: int) -> int:
        return completed_jobs * task.period
    
    def get_task_deadline(self, task: Task, release_time: int) -> int:
        return release_time + task.period
    
    def get_next_deadline_edf(self, current_time: int, task_states: dict) -> Tuple[Task, int]:
        earliest_deadline = float('inf')
        next_task = None
        next_release = None
        
        for task in self.tasks:
            jobs_completed = task_states[task.name]['completed']
            last_release = task_states[task.name]['last_release']
            
            # Calculate the next release time if task hasn't been released yet
            if last_release + task.period <= current_time:
                release_time = last_release + task.period
                absolute_deadline = release_time + task.period
                
                if absolute_deadline < earliest_deadline:
                    earliest_deadline = absolute_deadline
                    next_task = task
                    next_release = release_time
                    
        return next_task, next_release
    
    def get_next_task_rm(self, current_time: int, task_states: dict) -> Tuple[Task, int]:
        shortest_period = float('inf')
        next_task = None
        next_release = None
        
        sorted_tasks = sorted(self.tasks, key=lambda x: x.period)
        
        for task in sorted_tasks:
            jobs_completed = task_states[task.name]['completed']
            last_release = task_states[task.name]['last_release']
            
            if last_release + task.period <= current_time:
                if task.period < shortest_period:
                    shortest_period = task.period
                    next_task = task
                    next_release = last_release + task.period
                    
        return next_task, next_release
    
    def schedule_task(self, task: Task, current_time: int, energy_efficient: bool) -> Tuple[int, float]:
        if energy_efficient:
            deadline = current_time + task.period
            time_available = deadline - current_time
            
            viable_freqs = []
            for freq in self.cpu_power.frequencies:
                if task.wcet[freq] <= time_available:
                    energy = calculate_energy(self.cpu_power.active_power[freq], task.wcet[freq])
                    viable_freqs.append((freq, energy))
            
            if not viable_freqs:
                chosen_freq = self.cpu_power.frequencies[0]
            else:
                chosen_freq = min(viable_freqs, key=lambda x: x[1])[0]
        else:
            chosen_freq = self.cpu_power.frequencies[0]
        
        duration = task.wcet[chosen_freq]
        energy = calculate_energy(self.cpu_power.active_power[chosen_freq], duration)
        
        return chosen_freq, duration, energy
    
    def get_next_task_release(self, task_states: dict, current_time: int) -> int:
        next_release = float('inf')
        for task in self.tasks:
            last_release = task_states[task.name]['last_release']
            next_task_release = last_release + task.period
            if next_task_release > current_time:
                next_release = min(next_release, next_task_release)
        return next_release
    
    def run(self, policy: str, energy_efficient: bool = False):
        current_time = 0
        task_states = {task.name: {'completed': 0, 'last_release': -task.period} for task in self.tasks}
        
        while current_time < self.total_time:
            # Get next task based on policy
            if policy == "EDF":
                next_task, release_time = self.get_next_deadline_edf(current_time, task_states)
            else:  # RM
                next_task, release_time = self.get_next_task_rm(current_time, task_states)
            
            if next_task is None:
                # Find next release time
                next_release = self.get_next_task_release(task_states, current_time)
                
                if next_release < float('inf'):
                    idle_duration = next_release - current_time
                    idle_energy = calculate_energy(self.cpu_power.idle_power, idle_duration)
                    self.schedule.append((current_time, "IDLE", "IDLE", idle_duration, idle_energy))
                    current_time = next_release
                else:
                    # No more tasks to schedule
                    if current_time < self.total_time:
                        idle_duration = self.total_time - current_time
                        idle_energy = calculate_energy(self.cpu_power.idle_power, idle_duration)
                        self.schedule.append((current_time, "IDLE", "IDLE", idle_duration, idle_energy))
                        current_time = self.total_time
            else:
                # Schedule the task
                freq, duration, energy = self.schedule_task(next_task, current_time, energy_efficient)
                self.schedule.append((current_time, next_task.name, freq, duration, energy))
                current_time += duration
                task_states[next_task.name]['completed'] += 1
                task_states[next_task.name]['last_release'] = release_time
    
    def print_schedule(self):
        total_energy = 0
        idle_time = 0
        
        for start_time, task_name, freq, duration, energy in self.schedule:
            if task_name == "IDLE":
                idle_time += duration
            print(f"{start_time} {task_name} {freq} {duration} {energy:.3f}J")
            total_energy += energy
        
        print(f"\nTotal Energy Consumption: {total_energy:.3f}J")
        print(f"Percentage of time spent idle: {(idle_time/self.total_time)*100:.2f}%")
        print(f"Total System Execution Time: {self.total_time}s")

def main():
    if len(sys.argv) < 3:
        print("Usage: python scheduler.py <input_file> <EDF|RM> [EE]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    policy = sys.argv[2]
    energy_efficient = len(sys.argv) > 3 and sys.argv[3] == "EE"
    
    if policy not in ["EDF", "RM"]:
        print("Policy must be either EDF or RM")
        sys.exit(1)
    
    # Parse input and create scheduler
    tasks, cpu_power, total_time = parse_input(input_file)
    scheduler = Scheduler(tasks, cpu_power, total_time)
    
    # Run scheduling algorithm
    scheduler.run(policy, energy_efficient)
    
    # Print results
    scheduler.print_schedule()

if __name__ == "__main__":
    main()