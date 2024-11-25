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
    original_wcet: int
    policy: str
    period_start: int
    
    def __lt__(self, other):
        if self.policy == "EDF":
            if self.deadline != other.deadline:
                return self.deadline < other.deadline
            return self.period_start < other.period_start
        else:  # RM
            return self.task.period < other.task.period

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
        self.task_instances = {}
        self.next_releases = {}
        self.policy = None
        self.current_period = 0
        
        for task in tasks:
            self.next_releases[task.name] = 0
            self.task_instances[task.name] = None

    def should_preempt(self, current_task: TaskInstance, new_task: TaskInstance, current_time: int) -> bool:
        if self.policy == "EDF":
            if new_task.deadline < current_task.deadline:
                remaining_time = current_task.deadline - (current_time + current_task.remaining_time)
                return remaining_time > 0 and current_task.remaining_time > (current_task.deadline - new_task.deadline)
        elif self.policy == "RM":
            return new_task.task.period < current_task.task.period
        return False

    def create_task_instance(self, task: Task, release_time: int) -> TaskInstance:
        max_freq = self.cpu_power.frequencies[0]
        instance = TaskInstance(
            task=task,
            release_time=release_time,
            deadline=release_time + task.period,
            remaining_time=task.wcet[max_freq],
            original_wcet=task.wcet[max_freq],
            policy=self.policy,
            period_start=self.current_period
        )
        self.task_instances[task.name] = instance
        self.next_releases[task.name] = release_time + task.period
        return instance

    def get_next_release_time(self) -> Tuple[int, List[Task]]:
        next_time = float('inf')
        tasks_to_release = []
        
        for task in self.tasks:
            next_release = self.next_releases[task.name]
            
            if next_release < self.total_time and next_release > self.current_period:
                if next_release < next_time:
                    next_time = next_release
                    tasks_to_release = [task]
                elif next_release == next_time:
                    tasks_to_release.append(task)
        
        return next_time, tasks_to_release

    def find_best_frequency(self, task_instance: TaskInstance, current_time: int) -> Tuple[int, int]:
        if not task_instance:
            return self.cpu_power.frequencies[0], 0

        time_to_deadline = task_instance.deadline - current_time
        min_total_energy = float('inf')
        best_freq = self.cpu_power.frequencies[0]
        best_duration = task_instance.remaining_time
        
        if self.policy == "RM":
            next_high_priority = float('inf')
            for task in self.tasks:
                if task.period < task_instance.task.period:
                    next_release = self.next_releases[task.name]
                    if next_release > current_time and next_release < next_high_priority:
                        next_high_priority = next_release
            
            if next_high_priority < float('inf'):
                time_to_deadline = min(time_to_deadline, next_high_priority - current_time)
        
        for freq in self.cpu_power.frequencies:
            scaled_time = ceil(task_instance.remaining_time * 
                             (task_instance.task.wcet[freq] / task_instance.task.wcet[self.cpu_power.frequencies[0]]))
            
            if scaled_time <= time_to_deadline:
                active_energy = calculate_energy(self.cpu_power.active_power[freq], scaled_time)
                idle_time = time_to_deadline - scaled_time
                idle_energy = calculate_energy(self.cpu_power.idle_power, idle_time)
                total_energy = active_energy + idle_energy

                if total_energy < min_total_energy:
                    min_total_energy = total_energy
                    best_freq = freq
                    best_duration = scaled_time
        
        return best_freq, best_duration

    def get_execution_time(self, task: TaskInstance, current_time: int, next_release: int, chosen_freq: int) -> int:
        scaled_remaining = ceil(task.remaining_time * 
                              (task.task.wcet[chosen_freq] / task.task.wcet[self.cpu_power.frequencies[0]]))
        
        if self.policy == "RM":
            next_high_priority = float('inf')
            for task_check in self.tasks:
                if task_check.period < task.task.period:
                    next_release_check = self.next_releases[task_check.name]
                    if next_release_check > current_time and next_release_check < next_high_priority:
                        next_high_priority = next_release_check
            
            if next_high_priority < float('inf'):
                return min(scaled_remaining, next_high_priority - current_time)
        
        if next_release == float('inf') or scaled_remaining <= (next_release - current_time):
            return scaled_remaining
        
        return next_release - current_time

    def update_ready_queue(self, current_time: int, new_tasks: List[Task]) -> None:
        active_tasks = []
        
        while not self.ready_queue.empty():
            instance = self.ready_queue.get()
            if instance.remaining_time > 0 and instance.deadline > current_time:
                active_tasks.append(instance)
        
        for task in new_tasks:
            instance = TaskInstance(
                task=task,
                remaining_time=task.wcet[self.cpu_power.frequencies[0]],
                period_start=current_time,
                deadline=current_time + task.period,
                release_time=current_time,
                original_wcet=task.wcet[self.cpu_power.frequencies[0]],
                policy=self.policy
            )
            active_tasks.append(instance)
            self.next_releases[task.name] = current_time + task.period
        
        active_tasks.sort(key=lambda x: x.task.period)
        
        for instance in active_tasks:
            self.ready_queue.put(instance)

    def run(self, policy: str, energy_efficient: bool = False):
        self.policy = policy
        current_time = 0
        self.current_period = 0
        self.next_releases = {task.name: 0 for task in self.tasks}
        self.update_ready_queue(0, self.tasks)
        
        while current_time < self.total_time:
            next_release_time, next_release_tasks = self.get_next_release_time()
            current_task = None if self.ready_queue.empty() else self.ready_queue.get()
            
            if not current_task:
                idle_duration = min(next_release_time - current_time, self.total_time - current_time)
                if idle_duration > 0:
                    self.schedule.append((current_time, "IDLE", "IDLE", idle_duration,
                                       calculate_energy(self.cpu_power.idle_power, idle_duration)))
                current_time += idle_duration
            else:
                if energy_efficient:
                    chosen_freq, execution_time = self.find_best_frequency(current_task, current_time)
                else:
                    chosen_freq = self.cpu_power.frequencies[0]
                    execution_time = current_task.remaining_time
                
                if next_release_time < current_time + execution_time:
                    execution_time = next_release_time - current_time
                
                if current_time + execution_time > self.total_time:
                    execution_time = self.total_time - current_time
                
                energy = calculate_energy(self.cpu_power.active_power[chosen_freq], execution_time)
                self.schedule.append((current_time, current_task.task.name, chosen_freq,
                                    execution_time, energy))
                
                if chosen_freq != self.cpu_power.frequencies[0]:
                    progress = execution_time * (self.cpu_power.frequencies[0] / chosen_freq)
                    current_task.remaining_time -= progress
                else:
                    current_task.remaining_time -= execution_time
                
                if current_task.remaining_time > 0:
                    self.ready_queue.put(current_task)
                
                current_time += execution_time
            
            if current_time >= next_release_time and next_release_time < float('inf'):
                self.current_period = next_release_time
                self.update_ready_queue(next_release_time, next_release_tasks)

    def print_schedule(self):
        total_energy = 0
        idle_time = 0
        freq_distribution = {1188: 0, 918: 0, 648: 0, 384: 0, 'IDLE': 0}
        
        print("\nSchedule:")
        for start_time, task_name, freq, duration, energy in self.schedule:
            if task_name == "IDLE":
                idle_time += duration
                freq_distribution['IDLE'] += duration
            else:
                freq_distribution[freq] += duration
            print(f"{start_time} {task_name} {freq} {duration} {energy:.3f}J")
            total_energy += energy
        
        print(f"\nTotal Energy Consumption: {total_energy:.3f}J")
        print(f"Percentage of time spent idle: {(idle_time/self.total_time)*100:.2f}%")
        print(f"Total System Execution Time: {self.total_time}s")
        print("\nFrequency Distribution:")
        for freq, duration in freq_distribution.items():
            if duration > 0:
                print(f"{freq}: {duration}s ({(duration/self.total_time)*100:.2f}%)")

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