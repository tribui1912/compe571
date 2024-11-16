import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict
from queue import PriorityQueue
from math import ceil

@dataclass
class Task:
    name: str
    period: int
    wcet: dict[int, int]

@dataclass
class TaskInstance:
    task: Task
    release_time: int
    deadline: int
    remaining_time: int
    policy: str
    
    def __lt__(self, other):
        if self.policy == "EDF":
            return self.deadline < other.deadline  # EDF priority
        else:
            return self.task.period < other.task.period  # RM priority

@dataclass
class CPUPower:
    frequencies: List[int]
    active_power: dict[int, int]
    idle_power: int

def parse_input(filename: str) -> Tuple[List[Task], CPUPower, int]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    first_line = lines[0].strip().split()
    num_tasks = int(first_line[0])
    total_time = int(first_line[1])
    
    frequencies = [1188, 918, 648, 384]
    active_power = dict(zip(frequencies, map(int, first_line[2:6])))
    idle_power = int(first_line[6])
    cpu_power = CPUPower(frequencies, active_power, idle_power)
    
    tasks = []
    for i in range(num_tasks):
        line = lines[i + 1].strip().split()
        name = line[0]
        period = int(line[1])
        wcet = dict(zip(frequencies, map(int, line[2:])))
        tasks.append(Task(name, period, wcet))
    
    return tasks, cpu_power, total_time

def calculate_energy(power_mw: int, time_s: int) -> float:
    return (power_mw * time_s) / 1000.0

class Scheduler:
    def __init__(self, tasks: List[Task], cpu_power: CPUPower, total_time: int):
        self.tasks = tasks
        self.cpu_power = cpu_power
        self.total_time = total_time
        self.schedule = []
        self.ready_queue = PriorityQueue()
        self.task_instances = {}  # Store active task instances
        self.next_releases = {}   # Track next release time for each task
        self.policy = None
        
        # Initialize task tracking
        for task in tasks:
            self.next_releases[task.name] = 0
            self.task_instances[task.name] = None

    def create_task_instance(self, task: Task, release_time: int) -> TaskInstance:
        instance = TaskInstance(
            task=task,
            release_time=release_time,
            deadline=release_time + task.period,
            remaining_time=task.wcet[self.cpu_power.frequencies[0]],
            policy=self.policy
        )
        self.task_instances[task.name] = instance
        self.next_releases[task.name] = release_time + task.period
        return instance

    def get_next_release_time(self) -> Tuple[int, List[Task]]:
        next_time = float('inf')
        tasks_to_release = []
        
        for task in self.tasks:
            next_release = self.next_releases[task.name]
            if next_release < self.total_time:
                if next_release < next_time:
                    next_time = next_release
                    tasks_to_release = [task]
                elif next_release == next_time:
                    tasks_to_release.append(task)
                    
        return next_time, tasks_to_release

    def find_best_frequency(self, task_instance: TaskInstance, current_time: int) -> int:
        if not task_instance:
            return self.cpu_power.frequencies[0]
            
        time_available = task_instance.deadline - current_time
        min_energy = float('inf')
        best_freq = self.cpu_power.frequencies[0]
        
        for freq in self.cpu_power.frequencies:
            # Scale WCET and round up to nearest integer
            scaled_wcet = ceil(task_instance.remaining_time * (self.cpu_power.frequencies[0] / freq))
            if scaled_wcet <= time_available:
                active_energy = calculate_energy(self.cpu_power.active_power[freq], scaled_wcet)
                idle_time = time_available - scaled_wcet
                idle_energy = calculate_energy(self.cpu_power.idle_power, idle_time) if idle_time > 0 else 0
                total_energy = active_energy + idle_energy
                
                if total_energy < min_energy:
                    min_energy = total_energy
                    best_freq = freq
        
        return best_freq

    def update_ready_queue(self, current_time: int, new_tasks: List[Task]) -> None:
        for task in new_tasks:
            instance = self.create_task_instance(task, current_time)
            self.ready_queue.put(instance)
            
        active_tasks = []
        while not self.ready_queue.empty():
            instance = self.ready_queue.get()
            if instance.remaining_time > 0 and instance.deadline > current_time:
                active_tasks.append(instance)
                
        for instance in active_tasks:
            self.ready_queue.put(instance)

    def run(self, policy: str, energy_efficient: bool = False):
        self.policy = policy
        current_time = 0
        
        # Initial task releases at t=0
        self.update_ready_queue(0, self.tasks)
        
        while current_time < self.total_time:
            next_release_time, next_release_tasks = self.get_next_release_time()
            current_task = None if self.ready_queue.empty() else self.ready_queue.get()
            
            if not current_task:
                if next_release_time == float('inf') or next_release_time >= self.total_time:
                    idle_duration = self.total_time - current_time
                    if idle_duration > 0:
                        self.schedule.append((current_time, "IDLE", "IDLE", idle_duration, 
                                           calculate_energy(self.cpu_power.idle_power, idle_duration)))
                    break
                else:
                    idle_duration = next_release_time - current_time
                    self.schedule.append((current_time, "IDLE", "IDLE", idle_duration,
                                       calculate_energy(self.cpu_power.idle_power, idle_duration)))
                    current_time = next_release_time
                    self.update_ready_queue(current_time, next_release_tasks)
                    continue
            
            time_until_release = next_release_time - current_time if next_release_time < float('inf') else current_task.remaining_time
            
            if energy_efficient:
                chosen_freq = self.find_best_frequency(current_task, current_time)
            else:
                chosen_freq = self.cpu_power.frequencies[0]
            
            # Calculate execution time and round up to integer
            scale_factor = self.cpu_power.frequencies[0] / chosen_freq
            scaled_remaining = ceil(current_task.remaining_time * scale_factor)
            actual_duration = min(scaled_remaining, time_until_release)
            
            # Calculate execution progress (rounded up)
            execution_progress = ceil(actual_duration / scale_factor)
            current_task.remaining_time -= execution_progress
            
            energy = calculate_energy(self.cpu_power.active_power[chosen_freq], actual_duration)
            self.schedule.append((current_time, current_task.task.name, chosen_freq,
                                actual_duration, energy))
            
            if current_task.remaining_time > 0:
                self.ready_queue.put(current_task)
            
            current_time += actual_duration
            
            if current_time >= next_release_time:
                self.update_ready_queue(next_release_time, next_release_tasks)

    def print_schedule(self):
        total_energy = 0
        idle_time = 0
        
        print("\nSchedule:")
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
    
    tasks, cpu_power, total_time = parse_input(input_file)
    scheduler = Scheduler(tasks, cpu_power, total_time)
    scheduler.run(policy, energy_efficient)
    scheduler.print_schedule()

if __name__ == "__main__":
    main()