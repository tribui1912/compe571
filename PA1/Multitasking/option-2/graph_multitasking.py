import matplotlib.pyplot as plt
import re

def parse_results(filename):
    with open(filename, 'r') as f:
        content = f.read()

    pattern = r"Testing with N = (\d+) and processes = (\d+)\s+real\s+(\d+)m([\d.]+)s"
    matches = re.findall(pattern, content)

    data = {}
    for match in matches:
        N, processes, minutes, seconds = match
        N = int(N)
        processes = int(processes)
        time = float(minutes) * 60 + float(seconds)
        
        if N not in data:
            data[N] = {'processes': [], 'times': []}
        data[N]['processes'].append(processes)
        data[N]['times'].append(time)

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
                         xytext=(0,10), ha='center')

    plt.xlabel('Number of Processes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Number of Processes')
    plt.legend()
    plt.grid(True)
    plt.savefig('multitasking_performance.png')
    plt.close()

if __name__ == "__main__":
    data = parse_results('sum_multitasking_results.txt')
    create_graph(data)
    print("Graph has been saved as 'multitasking_performance.png'")