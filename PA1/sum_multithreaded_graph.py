import matplotlib.pyplot as plt
import re

# Initialize data structures
data = {100000000: {}, 1000000000: {}, 10000000000: {}}

# Read data from file
with open('sum_multithreaded_times.txt', 'r') as f:
    for line in f:
        match = re.match(r'N = (\d+), Threads = (\d+), Time = (\d+)m(\d+\.\d+)s', line)
        if match:
            n, threads, minutes, seconds = map(float, match.groups())
            time = minutes * 60 + seconds
            data[int(n)][int(threads)] = time

# Prepare plot
plt.figure(figsize=(12, 6))
markers = ['o', 's', '^']
colors = ['b', 'g', 'r']

# Plot data
for i, (n, thread_data) in enumerate(data.items()):
    threads = sorted(thread_data.keys())
    times = [thread_data[t] for t in threads]
    plt.plot(threads, times, marker=markers[i], color=colors[i], label=f'N = {n}')

# Customize plot
plt.xlabel('Number of Threads')
plt.ylabel('Execution Time (seconds)')
plt.title('Multithreaded Sum Execution Time')
plt.legend()
plt.grid(True)
plt.xscale('log', base=2)
plt.yscale('log')

# Save plot
plt.savefig('multithreaded_sum_performance.png')
plt.close()

print("Graph has been saved as 'multithreaded_sum_performance.png'")