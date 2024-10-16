import matplotlib.pyplot as plt
import numpy as np
import re

def parse_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    data = {}
    current_program = None
    for line in content.split('\n'):
        if line.startswith('Running'):
            current_program = line.split('...')[0].split()[-1]
            data[current_program] = []
        elif 'Response time for' in line:
            workload = line.split()[3]
            time = int(line.split()[-2])
            data[current_program].append((workload, time))
    
    return data

# Parse all files
all_data = [parse_file(f'response_times_{i}.txt') for i in range(5)]

# Prepare data for plotting
programs = ['sample_program', 'SJF_implementation', 'FCFS_implementation', 'MLFQ_implementation']
workloads = ['WORKLOAD1', 'WORKLOAD2', 'WORKLOAD3', 'WORKLOAD4']
colors = ['red', 'green', 'blue', 'purple']

# Find global min and max response times
global_min = float('inf')
global_max = float('-inf')
for data in all_data:
    for program in programs:
        for _, time in data[program]:
            global_min = min(global_min, time)
            global_max = max(global_max, time)

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 15))
fig.suptitle('Response Times for Different Scheduling Algorithms', fontsize=16)

for idx, program in enumerate(programs):
    ax = axs[idx // 2, idx % 2]
    
    for workload_idx, workload in enumerate(workloads):
        times = [data[program][workload_idx][1] for data in all_data]
        ax.scatter(range(5), times, color=colors[workload_idx], label=workload)
        ax.plot(range(5), times, color=colors[workload_idx], alpha=0.5)
    
    ax.set_title(program)
    ax.set_xlabel('Run Number')
    ax.set_ylabel('Response Time (microseconds)')
    ax.set_xticks(range(5))
    ax.set_yscale('log')  # Set logarithmic scale for y-axis
    ax.set_ylim(max(1, global_min), global_max * 1.1)  # Set y-axis limits, avoiding 0
    ax.legend()

plt.tight_layout()

# Save the graph
output_path = 'response_times_graph.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_path}")

# Remove the comment to display the graph
# plt.show()
