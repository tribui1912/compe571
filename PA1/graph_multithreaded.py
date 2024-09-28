import matplotlib.pyplot as plt
import re
import os

def parse_results(filename):
    with open(filename, 'r') as f:
        content = f.read()

    pattern = r"Testing with N = (\d+) and threads = (\d+)\s+real\s+(\d+)m([\d.]+)s"
    matches = re.findall(pattern, content)

    data = {}
    for match in matches:
        N, threads, minutes, seconds = match
        N = int(N)
        threads = int(threads)
        time = float(minutes) * 60 + float(seconds)
        
        if N not in data:
            data[N] = {'threads': [], 'times': []}
        data[N]['threads'].append(threads)
        data[N]['times'].append(round(time, 3))

    return data

def create_graph(data):
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r']
    markers = ['o', 's', '^']

    for i, (N, values) in enumerate(data.items()):
        plt.plot(values['threads'], values['times'], 
                 color=colors[i % len(colors)], 
                 marker=markers[i % len(markers)], 
                 label=f'N = {N}')

        for x, y in zip(values['threads'], values['times']):
            plt.annotate(f'{y:.3f}', (x, y), textcoords="offset points", 
                         xytext=(0,10), ha='center', fontsize=8)

    plt.xlabel('Number of Threads')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Multithreaded Performance')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xticks([2, 4, 8])
    plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter())
    plt.tight_layout()
    plt.savefig('multithreaded_performance.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    file_path = 'sum_multithreaded_results.txt'
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        print(f"Current working directory: {os.getcwd()}")
        exit(1)

    data = parse_results(file_path)
    create_graph(data)
    print("Graph has been saved as 'multithreaded_performance.png'")