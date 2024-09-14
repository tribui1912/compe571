import re
import matplotlib.pyplot as plt
import math


### Parsing the file for graph data 
def parse_results(filename):
    results = {}
    current_n = None
    current_threads = None
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Testing with N ="):
                match = re.search(r'N = (\d+) and threads = (\d+)', line)
                if match:
                    current_n = int(match.group(1))
                    current_threads = int(match.group(2))
                    if current_n not in results:
                        results[current_n] = {}
            elif line.startswith("real"):
                time_parts = line.split()
                if len(time_parts) > 1:
                    time_str = time_parts[1]
                    try:
                        minutes, seconds = time_str.split('m')
                        seconds = seconds.rstrip('s')
                        time = float(minutes) * 60 + float(seconds)
                        if current_n is not None and current_threads is not None:
                            results[current_n][current_threads] = time
                    except ValueError as e:
                        print(f"Error parsing time: {time_str}. Error: {e}")
    
    return results

### Plot the data
def plot_results(results):
    plt.figure(figsize=(12, 7))
    
    for n in sorted(results.keys()):
        thread_counts = sorted(results[n].keys())
        times = [results[n][t] for t in thread_counts]
        plt.plot(thread_counts, times, marker='o', label=f'N = 10^{int(math.log10(n))}')
    
    plt.xlabel('Number of Threads')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Multithreaded Sum Performance')
    plt.legend()
    plt.xscale('linear')
    plt.yscale('log')
    plt.xticks([2, 4, 8])
    plt.grid(True)
    plt.savefig('sum_multithreaded_performance.png')
    plt.close()

# Main execution
try:
    results = parse_results('sum_multithreaded_results.txt')
    if not results:
        raise ValueError("No data was parsed from the file")
    plot_results(results)
    print("Graph has been saved as 'sum_multithreaded_performance.png'")
except Exception as e:
    print(f"An error occurred: {e}")
