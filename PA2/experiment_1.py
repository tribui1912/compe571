import statistics
import matplotlib.pyplot as plt

def parse_results(filename):
    results = {}
    current_quantum = None
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Quantum:"):
                current_quantum = int(line.split()[1])
                results[current_quantum] = []
            elif "Average response time:" in line:
                response_time = float(line.split()[-2])
                results[current_quantum].append(response_time)
    return results

def process_results(results):
    processed = []
    for quantum, times in results.items():
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        processed.append((quantum, avg_time, std_dev))
    return processed

def plot_results(results):
    quanta, avg_times, std_devs = zip(*results)
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(quanta, avg_times, yerr=std_devs, fmt='o-', capsize=5)
    
    # Add labels for each data point
    for quantum, avg_time in zip(quanta, avg_times):
        plt.annotate(f'{quantum}', (quantum, avg_time), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.xscale('log')
    plt.xlabel('Quantum (µs)')
    plt.ylabel('Average Response Time (µs)')
    plt.title('Average Response Time vs Quantum')
    plt.grid(True)
    plt.savefig('quantum_results.png')
    print("Plot saved as quantum_results.png")

if __name__ == "__main__":
    input_file = "experiment_1.txt"
    results = parse_results(input_file)
    processed_results = process_results(results)
    plot_results(processed_results)

    best_quantum = min(processed_results, key=lambda x: x[1])
    print(f"\nBest quantum found: {best_quantum[0]} µs")
    print(f"Best average response time: {best_quantum[1]:.2f} µs")
