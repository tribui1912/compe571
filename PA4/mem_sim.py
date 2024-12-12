import argparse
from dataclasses import dataclass
from enum import Enum
import random
from typing import Dict, List, Optional, Set, Tuple

class AccessType(Enum):
    READ = 'R'
    WRITE = 'W'

@dataclass
class MemoryReference:
    process_id: int
    address: int
    access_type: AccessType
    
    @classmethod
    def from_line(cls, line: str) -> 'MemoryReference':
        pid, addr, access = line.strip().split()
        return cls(int(pid), int(addr), AccessType(access))

@dataclass
class SimulationResult:
    algorithm: str
    page_faults: int
    disk_references: int
    dirty_writes: int

    def __str__(self) -> str:
        return (f"\n{self.algorithm} Algorithm Results:\n"
                f"Page Faults: {self.page_faults}\n"
                f"Disk References: {self.disk_references}\n"
                f"Dirty Page Writes: {self.dirty_writes}")

class Process:
    def __init__(self, pid: int):
        self.pid = pid
        self.page_table: List[PageTableEntry] = [
            PageTableEntry(i, None) for i in range(128)  # 128 pages per process
        ]

@dataclass
class PageTableEntry:
    virtual_page: int
    physical_frame: Optional[int]
    dirty: bool = False
    referenced: bool = False
    last_access_time: int = 0

class MemorySystem:
    PAGE_SIZE = 512  # bytes
    PHYSICAL_PAGES = 32
    REFERENCE_RESET_INTERVAL = 200

    def __init__(self, algorithm: str):
        self.algorithm = algorithm.upper()
        self.processes: Dict[int, Process] = {}
        self.physical_memory: List[Tuple[int, int]] = []  # List of (pid, vpn) pairs
        self.time = 0
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_writes = 0
        self.references_since_reset = 0

    def get_page_number(self, address: int) -> int:
        return address >> 9  # Get the 7 most significant bits

    def get_process(self, pid: int) -> Process:
        if pid not in self.processes:
            self.processes[pid] = Process(pid)
        return self.processes[pid]

    def handle_memory_access(self, ref: MemoryReference) -> None:
        self.time += 1
        self.references_since_reset += 1
        
        if self.references_since_reset == self.REFERENCE_RESET_INTERVAL and self.algorithm == 'PER':
            self.reset_reference_bits()
            self.references_since_reset = 0

        process = self.get_process(ref.process_id)
        page_number = self.get_page_number(ref.address)
        page_entry = process.page_table[page_number]

        if page_entry.physical_frame is None:
            self.handle_page_fault(process, page_number)

        page_entry.referenced = True
        page_entry.last_access_time = self.time
        if ref.access_type == AccessType.WRITE:
            page_entry.dirty = True

    def handle_page_fault(self, process: Process, page_number: int) -> None:
        self.page_faults += 1
        self.disk_references += 1

        if len(self.physical_memory) < self.PHYSICAL_PAGES:
            frame_number = len(self.physical_memory)
            self.physical_memory.append((process.pid, page_number))
            process.page_table[page_number].physical_frame = frame_number
        else:
            victim_frame = self.select_victim_page()
            victim_pid, victim_vpn = self.physical_memory[victim_frame]
            victim_process = self.processes[victim_pid]
            victim_page = victim_process.page_table[victim_vpn]

            if victim_page.dirty:
                self.disk_references += 1
                self.dirty_writes += 1

            victim_page.physical_frame = None
            process.page_table[page_number].physical_frame = victim_frame
            self.physical_memory[victim_frame] = (process.pid, page_number)

    def select_victim_page(self) -> int:
        if self.algorithm == 'RAND':
            return random.randrange(self.PHYSICAL_PAGES)
        
        elif self.algorithm == 'FIFO':
            return 0  # Always replace the first page (rotate the list after)
        
        elif self.algorithm == 'LRU':
            min_time = float('inf')
            victim_frame = 0
            for frame, (pid, vpn) in enumerate(self.physical_memory):
                page = self.processes[pid].page_table[vpn]
                if page.last_access_time < min_time:
                    min_time = page.last_access_time
                    victim_frame = frame
                elif page.last_access_time == min_time:
                    current_dirty = self.processes[pid].page_table[vpn].dirty
                    victim_dirty = self.processes[self.physical_memory[victim_frame][0]].page_table[self.physical_memory[victim_frame][1]].dirty
                    if (not current_dirty and victim_dirty) or (current_dirty == victim_dirty and frame < victim_frame):
                        victim_frame = frame
            return victim_frame
        
        elif self.algorithm == 'PER':
            categories = [
                (False, False),  # unreferenced, clean
                (False, True),   # unreferenced, dirty
                (True, False),   # referenced, clean
                (True, True)     # referenced, dirty
            ]
            
            for ref_bit, dirty_bit in categories:
                min_frame = float('inf')
                for frame, (pid, vpn) in enumerate(self.physical_memory):
                    page = self.processes[pid].page_table[vpn]
                    if page.referenced == ref_bit and page.dirty == dirty_bit:
                        min_frame = min(min_frame, frame)
                if min_frame != float('inf'):
                    return min_frame
            
            return 0

    def reset_reference_bits(self) -> None:
        for process in self.processes.values():
            for page in process.page_table:
                page.referenced = False

def simulate(input_file: str, algorithm: str) -> SimulationResult:
    system = MemorySystem(algorithm)
    
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                ref = MemoryReference.from_line(line)
                system.handle_memory_access(ref)
                
                if algorithm == 'FIFO' and len(system.physical_memory) == system.PHYSICAL_PAGES:
                    system.physical_memory = system.physical_memory[1:] + [system.physical_memory[0]]
    
    return SimulationResult(
        algorithm=algorithm,
        page_faults=system.page_faults,
        disk_references=system.disk_references,
        dirty_writes=system.dirty_writes
    )

def main():
    parser = argparse.ArgumentParser(description='Virtual Memory Simulator')
    parser.add_argument('input_file', help='Path to the input file containing memory references')
    parser.add_argument('--algorithms', nargs='+', 
                      choices=['RAND', 'FIFO', 'LRU', 'PER'],
                      default=['RAND', 'FIFO', 'LRU', 'PER'],
                      help='Page replacement algorithms to simulate')
    
    args = parser.parse_args()
    
    print(f"\nRunning simulation with input file: {args.input_file}")
    print("Page size: 512 bytes")
    print("Physical memory size: 16KB (32 pages)")
    print("Virtual address space per process: 64KB (128 pages)\n")
    
    for algorithm in args.algorithms:
        result = simulate(args.input_file, algorithm)
        print(result)

if __name__ == "__main__":
    main()