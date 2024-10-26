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
            workload = line.split()[3].strip(':')
            time = int(line.split()[-2])
            data[current_program].append((workload, time))
    
    return data

# Parse all files
all_data = [parse_file(f'response_times_{i}.txt') for i in range(6)]

# Prepare data for plotting
programs = ['sample_program', 'SJF_implementation', 'FCFS_implementation', 'MLFQ_implementation']
workloads = ['WORKLOAD1', 'WORKLOAD2', 'WORKLOAD3', 'WORKLOAD4']
colors = {'sample_program': 'red', 'SJF_implementation': 'green', 'FCFS_implementation': 'blue', 'MLFQ_implementation': 'purple'}

# Calculate total response time for each algorithm
total_response_times = {program: [] for program in programs}

for data in all_data:
    for program in programs:
        total_time = sum(time for _, time in data[program])
        total_response_times[program].append(total_time)

# Calculate and print average and standard deviation for each implementation
for program in programs:
    avg = np.mean(total_response_times[program]) / 1000  # Convert to milliseconds
    std_dev = np.std(total_response_times[program]) / 1000  # Convert to milliseconds
    std_dev_percent = (std_dev / avg) * 100  # Calculate std dev as percentage of mean
    print(f"{program}:")
    print(f"  Average: {avg:.2f} milliseconds")
    print(f"  Standard deviation: {std_dev:.2f} milliseconds ({std_dev_percent:.2f}%)")
    print()

# Create the plot
plt.figure(figsize=(12, 8))
plt.title('Total Response Times for Different Scheduling Algorithms', fontsize=16)

for program in programs:
    plt.plot(range(6), total_response_times[program], color=colors[program], label=program, marker='o')

plt.xlabel('Run Number')
plt.ylabel('Total Response Time (microseconds)')
plt.xticks(range(6))
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Set y-axis to logarithmic scale
plt.yscale('log')

# Adjust layout and save the graph
plt.tight_layout()
output_path = 'total_response_times_graph.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_path}")

# Remove the comment to display the graph
# plt.show()
