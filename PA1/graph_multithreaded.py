import matplotlib.pyplot as plt
import re

def parse_results(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Regular expression to extract N, thread count, and execution time
    pattern = r"Testing with N = (\d+) and threads = (\d+)\s+real\s+(\d+)m([\d.]+)s"
    matches = re.findall(pattern, content)

    data = {}
    for match in matches:
        N, threads, minutes, seconds = match
        N = int(N)
        threads = int(threads)
        # Convert time to seconds
        time = float(minutes) * 60 + float(seconds)
        
        if N not in data:
            data[N] = {'threads': [], 'times': []}
        data[N]['threads'].append(threads)
        data[N]['times'].append(time)

    return data

# Parse the results
data = parse_results('sum_multithreaded_results.txt')

# Plotting execution time
plt.figure(figsize=(12, 7))
for N, values in data.items():
    line, = plt.plot(values['threads'], values['times'], marker='o', label=f'N={N}')
    for x, y in zip(values['threads'], values['times']):
        # Annotate each point with the time value (3 decimal places)
        plt.annotate(f'{y:.3f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Number of Threads')
plt.ylabel('Execution Time (seconds)')
plt.title('Multithreaded Sum Performance')
plt.legend()
plt.xscale('log', base=2)  # Use log scale for x-axis
plt.yscale('log')  # Use log scale for y-axis
plt.grid(True)
plt.tight_layout()

plt.savefig('sum_performance.png', dpi=300)
plt.close()

# Plotting speedup
plt.figure(figsize=(12, 7))
for N, values in data.items():
    baseline = values['times'][0]  # Time for 2 threads (first entry)
    speedup = [baseline / t for t in values['times']]
    line, = plt.plot(values['threads'], speedup, marker='o', label=f'N={N}')
    for x, y in zip(values['threads'], speedup):
        # Annotate each point with the speedup value (3 decimal places)
        plt.annotate(f'{y:.3f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.title('Speedup vs Number of Threads')
plt.legend()
plt.xscale('log', base=2)  # Use log scale for x-axis
plt.grid(True)
plt.tight_layout()

plt.savefig('multithreaded_performance.png', dpi=300)
plt.close()