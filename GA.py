import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Job:
    id: int
    name: str
    processing_times: List[int]
    priority: int = 1

class JobSchedulingGA:
    def __init__(self, jobs: List[Job], num_machines: int, population_size: int = 50,
                 elite_size: int = 10, mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.jobs = jobs
        self.num_machines = num_machines
        self.num_jobs = len(jobs)
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.best_individual = None
        self.best_fitness = float('inf')
        self.fitness_history = []
    
    def create_individual(self) -> List[Tuple[int, int]]:
        return [(job_idx, random.randint(0, self.num_machines - 1)) 
                for job_idx in range(self.num_jobs)]
    
    def create_population(self) -> List[List[Tuple[int, int]]]:
        return [self.create_individual() for _ in range(self.population_size)]
    
    def calculate_fitness(self, individual: List[Tuple[int, int]]) -> float:
        machine_times = [0] * self.num_machines
        
        for job_idx, machine_idx in individual:
            job = self.jobs[job_idx]
            processing_time = job.processing_times[machine_idx]
            priority_penalty = (6 - job.priority) * 2
            machine_times[machine_idx] += processing_time + priority_penalty
        
        makespan = max(machine_times)
        avg_load = sum(machine_times) / len(machine_times)
        load_variance = sum((t - avg_load) ** 2 for t in machine_times) / len(machine_times)
        
        return makespan + 0.1 * load_variance
    
    def tournament_selection(self, population: List[List[Tuple[int, int]]], k: int = 3):
        tournament = random.sample(population, k)
        return min(tournament, key=self.calculate_fitness)
    
    def order_crossover(self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        # Child 1
        child1 = [None] * size
        child1[start:end+1] = parent1[start:end+1]
        used_jobs = {parent1[i][0] for i in range(start, end+1)}
        remaining = [x for x in parent2 if x[0] not in used_jobs]
        
        j = 0
        for i in range(size):
            if child1[i] is None:
                child1[i] = remaining[j]
                j += 1
        
        # Child 2
        child2 = [None] * size
        child2[start:end+1] = parent2[start:end+1]
        used_jobs = {parent2[i][0] for i in range(start, end+1)}
        remaining = [x for x in parent1 if x[0] not in used_jobs]
        
        j = 0
        for i in range(size):
            if child2[i] is None:
                child2[i] = remaining[j]
                j += 1
        
        return child1, child2
    
    def swap_mutation(self, individual: List[Tuple[int, int]]):
        mutated = individual.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                if random.random() < 0.5:
                    j = random.randint(0, len(mutated) - 1)
                    mutated[i], mutated[j] = mutated[j], mutated[i]
                else:
                    job_id = mutated[i][0]
                    new_machine = random.randint(0, self.num_machines - 1)
                    mutated[i] = (job_id, new_machine)
        
        return mutated
    
    def evolve_generation(self, population: List[List[Tuple[int, int]]]):
        sorted_pop = sorted(population, key=self.calculate_fitness)
        new_population = sorted_pop[:self.elite_size].copy()
        
        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            child1, child2 = self.order_crossover(parent1, parent2)
            child1 = self.swap_mutation(child1)
            child2 = self.swap_mutation(child2)
            new_population.extend([child1, child2])
        
        return new_population[:self.population_size]
    
    def solve(self, max_generations: int = 100, verbose: bool = True):
        population = self.create_population()
        self.best_individual = min(population, key=self.calculate_fitness)
        self.best_fitness = self.calculate_fitness(self.best_individual)
        self.fitness_history = [self.best_fitness]
        
        if verbose:
            print(f"Thế hệ 0 - Fitness tốt nhất: {self.best_fitness:.2f}")
        
        for generation in range(1, max_generations + 1):
            population = self.evolve_generation(population)
            current_best = min(population, key=self.calculate_fitness)
            current_fitness = self.calculate_fitness(current_best)
            
            if current_fitness < self.best_fitness:
                self.best_fitness = current_fitness
                self.best_individual = current_best.copy()
            
            self.fitness_history.append(self.best_fitness)
            
            if verbose and generation % 10 == 0:
                print(f"Thế hệ {generation} - Fitness tốt nhất: {self.best_fitness:.2f}")
        
        return self.best_individual, self.best_fitness
    
    def print_solution(self):
        if self.best_individual is None:
            print("Chưa có solution. Hãy chạy solve() trước.")
            return
        
        print("\n=== LỊCH TRÌNH TỐI ƯU ===")
        
        machine_schedules = [[] for _ in range(self.num_machines)]
        machine_times = [0] * self.num_machines
        
        for job_idx, machine_idx in self.best_individual:
            job = self.jobs[job_idx]
            processing_time = job.processing_times[machine_idx]
            
            machine_schedules[machine_idx].append({
                'job': job,
                'start_time': machine_times[machine_idx],
                'end_time': machine_times[machine_idx] + processing_time
            })
            
            machine_times[machine_idx] += processing_time
        
        for i, schedule in enumerate(machine_schedules):
            print(f"\nMáy {i+1} (Tổng thời gian: {machine_times[i]}):")
            for task in schedule:
                job = task['job']
                print(f"  Job {job.id} ({job.name}) - Độ ưu tiên {job.priority}")
                print(f"    Thời gian: {task['start_time']} -> {task['end_time']} ({task['end_time'] - task['start_time']} đơn vị)")
        
        print(f"\nMakespan: {max(machine_times)}")
        print(f"Fitness: {self.best_fitness:.2f}")
    
    def plot_convergence(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.fitness_history, 'b-', linewidth=2)
        plt.title('Biểu đồ hội tụ GA')
        plt.xlabel('Thế hệ')
        plt.ylabel('Fitness tốt nhất')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plot_gantt_chart(self):
        if self.best_individual is None:
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        machine_schedules = [[] for _ in range(self.num_machines)]
        machine_times = [0] * self.num_machines
        
        for job_idx, machine_idx in self.best_individual:
            job = self.jobs[job_idx]
            processing_time = job.processing_times[machine_idx]
            start_time = machine_times[machine_idx]
            
            machine_schedules[machine_idx].append({
                'job': job,
                'start_time': start_time,
                'end_time': start_time + processing_time,
                'duration': processing_time
            })
            
            machine_times[machine_idx] += processing_time
        
        colors = plt.cm.Set3(np.linspace(0, 1, self.num_jobs))
        
        for machine_idx, schedule in enumerate(machine_schedules):
            for task in schedule:
                job = task['job']
                ax.barh(machine_idx, task['duration'], 
                       left=task['start_time'], 
                       color=colors[job.id], 
                       alpha=0.8,
                       edgecolor='black')
                ax.text(task['start_time'] + task['duration']/2, machine_idx,
                       f'J{job.id}', ha='center', va='center', fontweight='bold')
        
        ax.set_xlabel('Thời gian')
        ax.set_ylabel('Máy')
        ax.set_title('Biểu đồ Gantt - Lịch trình Sản xuất')
        ax.set_yticks(range(self.num_machines))
        ax.set_yticklabels([f'Máy {i+1}' for i in range(self.num_machines)])
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

def create_sample_jobs():
    return [
        Job(0, "Sản xuất linh kiện A", [5, 3, 7, 4], priority=3),
        Job(1, "Gia công sản phẩm B", [2, 8, 4, 6], priority=5),
        Job(2, "Lắp ráp máy C", [6, 2, 3, 9], priority=2),
        Job(3, "Kiểm tra chất lượng D", [3, 5, 8, 2], priority=4),
        Job(4, "Đóng gói sản phẩm E", [4, 7, 2, 5], priority=1),
        Job(5, "Vận chuyển F", [1, 4, 6, 3], priority=3),
    ]

def input_custom_jobs():
    num_machines = int(input("Nhập số lượng máy: "))
    num_jobs = int(input("Nhập số lượng công việc: "))
    
    jobs = []
    for i in range(num_jobs):
        print(f"\nCông việc {i+1}:")
        name = input(f"Tên công việc: ").strip() or f"Job_{i+1}"
        priority = int(input("Độ ưu tiên (1-5): "))
        
        processing_times = []
        print("Nhập thời gian xử lý trên từng máy:")
        for j in range(num_machines):
            time = int(input(f"  Máy {j+1}: "))
            processing_times.append(time)
        
        jobs.append(Job(i, name, processing_times, priority))
    
    return jobs, num_machines

def main():
    print("=== GIẢI THUẬT DI TRUYỀN CHO BÀI TOÁN LẬP LỊCH ===")
    print("1. Sử dụng dữ liệu mẫu")
    print("2. Nhập dữ liệu tùy chỉnh")
    
    choice = input("Chọn (1/2): ").strip()
    
    if choice == '1':
        jobs = create_sample_jobs()
        num_machines = 4
        print(f"Sử dụng {len(jobs)} công việc và {num_machines} máy")
    else:
        jobs, num_machines = input_custom_jobs()
    
    print("\nCấu hình Genetic Algorithm:")
    population_size = int(input("Kích thước quần thể (50): ") or 50)
    max_generations = int(input("Số thế hệ tối đa (100): ") or 100)
    mutation_rate = float(input("Tỷ lệ đột biến (0.1): ") or 0.1)
    
    ga = JobSchedulingGA(
        jobs=jobs,
        num_machines=num_machines,
        population_size=population_size,
        mutation_rate=mutation_rate
    )
    
    print(f"\nĐang giải bài toán với GA...")
    print(f"Tham số: Pop={population_size}, Gen={max_generations}, Mutation={mutation_rate}")
    
    best_schedule, best_fitness = ga.solve(max_generations, verbose=True)
    ga.print_solution()
    
    show_plots = input("\nBạn có muốn xem biểu đồ? (y/n): ").lower() == 'y'
    if show_plots:
        ga.plot_convergence()
        ga.plot_gantt_chart()

if __name__ == "__main__":
    main()
