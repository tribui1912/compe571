import matplotlib.pyplot as plt
import re
import os

def parse_results(filename):
    with open(filename, 'r') as f:
        content = f.read()

    pattern = r"Testing with N = (\d+) and num_processes = (\d+).*?real\s+(\d+)m([\d.]+)s"
    matches = re.findall(pattern, content, re.DOTALL)

    data = {}
    for match in matches:
        N, processes, minutes, seconds = match
        N = int(N)
        processes = int(processes)
        time = float(minutes) * 60 + float(seconds)
        
        if N not in data:
            data[N] = {'processes': [], 'times': []}
        data[N]['processes'].append(processes)
        data[N]['times'].append(round(time, 3))

    return data

def create_graph(data):
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r']
    markers = ['o', 's', '^']

    for i, (N, values) in enumerate(data.items()):
        plt.plot(values['processes'], values['times'], 
                 color=colors[i % len(colors)], 
                 marker=markers[i % len(markers)], 
                 label=f'N = {N}')

        for x, y in zip(values['processes'], values['times']):
            plt.annotate(f'{y:.3f}', (x, y), textcoords="offset points", 
                         xytext=(0,10), ha='center', fontsize=8)

    plt.xlabel('Number of Processes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Multitasking Performance')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xticks([2, 4, 8])
    plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter())
    plt.tight_layout()
    plt.savefig('multitasking_performance_1.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    file_path = 'sum_multitasking_1_results.txt'
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        print(f"Current working directory: {os.getcwd()}")
        exit(1)

    data = parse_results(file_path)
    create_graph(data)
    print("Graph has been saved as 'multitasking_performance_1.png'")