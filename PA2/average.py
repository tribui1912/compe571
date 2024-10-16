import matplotlib.pyplot as plt
import numpy as np

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
            workload = line.split()[3].strip(':')  # Remove any trailing colon
            time = int(line.split()[-2])
            data[current_program].append((workload, time))
    
    return data

# Parse all files
all_data = [parse_file(f'response_times_{i}.txt') for i in range(6)]

# Prepare data for plotting
programs = ['sample_program', 'SJF_implementation', 'FCFS_implementation', 'MLFQ_implementation']
workloads = ['WORKLOAD1', 'WORKLOAD2', 'WORKLOAD3', 'WORKLOAD4']
colors = {'WORKLOAD1': 'red', 'WORKLOAD2': 'green', 'WORKLOAD3': 'blue', 'WORKLOAD4': 'purple'}

# Calculate average response times
avg_data = {}
for program in programs:
    avg_data[program] = []
    for workload_idx in range(4):
        avg_time = np.mean([data[program][workload_idx][1] for data in all_data])
        avg_data[program].append((workloads[workload_idx], avg_time))

# Find global min and max average response times
global_min = float('inf')
global_max = float('-inf')
for program in programs:
    for _, time in avg_data[program]:
        global_min = min(global_min, time)
        global_max = max(global_max, time)

# Create bar plot
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Average Response Times for Different Scheduling Algorithms', fontsize=16)

bar_width = 0.2
index = np.arange(4)

for i, program in enumerate(programs):
    avg_times = [time for _, time in avg_data[program]]
    ax.bar(index + i * bar_width, avg_times, bar_width, label=program, alpha=0.8)

ax.set_xlabel('Workload')
ax.set_ylabel('Average Response Time (microseconds)')
ax.set_xticks(index + bar_width * 1.5)
ax.set_xticklabels(workloads)
ax.legend()
ax.set_yscale('log')
ax.set_ylim(max(1, global_min * 0.9), global_max * 1.1)

plt.tight_layout()

# Save the graph
output_path = 'average_response_times_graph.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_path}")

# Remove the comment to display the graph
# plt.show()