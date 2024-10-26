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
            data[current_program] = {}
        elif 'Total context switch time:' in line:
            data[current_program]['total_time'] = int(line.split()[-2])
        elif 'Number of context switches:' in line:
            data[current_program]['switch_count'] = int(line.split()[-1])
        elif 'Average context switch time:' in line:
            data[current_program]['avg_time'] = float(line.split()[-2])
    
    return data

# Parse all files
all_data = [parse_file(f'context_switch_{i}.txt') for i in range(6)]

# Prepare data for plotting
programs = ['sample_program', 'SJF_implementation', 'FCFS_implementation', 'MLFQ_implementation']
colors = {'sample_program': 'red', 'SJF_implementation': 'green', 'FCFS_implementation': 'blue', 'MLFQ_implementation': 'purple'}

# Calculate statistics for each algorithm
switch_counts = {program: [] for program in programs}
avg_switch_times = {program: [] for program in programs}
total_switch_times = {program: [] for program in programs}

for data in all_data:
    for program in programs:
        switch_counts[program].append(data[program]['switch_count'])
        avg_switch_times[program].append(data[program]['avg_time'])
        total_switch_times[program].append(data[program]['total_time'])

# Calculate and print average and standard deviation for each implementation
for program in programs:
    avg_count = np.mean(switch_counts[program])
    std_dev_count = np.std(switch_counts[program])
    avg_time = np.mean(avg_switch_times[program])
    std_dev_time = np.std(avg_switch_times[program])
    avg_total_time = np.mean(total_switch_times[program])
    std_dev_total_time = np.std(total_switch_times[program])
    
    print(f"{program}:")
    print(f"  Average switch count: {avg_count:.2f}")
    print(f"  Switch count std dev: {std_dev_count:.2f} ({(std_dev_count/avg_count)*100:.2f}%)")
    print(f"  Average switch time: {avg_time:.2f} microseconds")
    print(f"  Switch time std dev: {std_dev_time:.2f} microseconds ({(std_dev_time/avg_time)*100:.2f}%)")
    print(f"  Average total switch time: {avg_total_time:.2f} microseconds")
    print(f"  Total switch time std dev: {std_dev_total_time:.2f} microseconds ({(std_dev_total_time/avg_total_time)*100:.2f}%)")
    print()

# Function to create and save a plot
def create_plot(data, title, ylabel, filename):
    plt.figure(figsize=(12, 8))
    plt.title(title, fontsize=16)

    for program in programs:
        plt.plot(range(6), data[program], color=colors[program], label=program, marker='o')

    plt.xlabel('Run Number')
    plt.ylabel(ylabel)
    plt.xticks(range(6))
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.yscale('log')  # Set y-axis to logarithmic scale

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Graph saved to {filename}")
    plt.close()

# Create and save plots
create_plot(switch_counts, 'Context Switch Counts for Different Scheduling Algorithms', 
            'Number of Context Switches (log scale)', 'context_switch_counts_graph.png')

create_plot(avg_switch_times, 'Average Context Switch Times for Different Scheduling Algorithms', 
            'Average Context Switch Time (microseconds, log scale)', 'average_context_switch_times_graph.png')

create_plot(total_switch_times, 'Total Context Switch Times for Different Scheduling Algorithms', 
            'Total Context Switch Time (microseconds, log scale)', 'total_context_switch_times_graph.png')

# Remove the comment to display the graphs
# plt.show()
