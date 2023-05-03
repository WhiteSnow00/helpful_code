import random

# Đầu vào
population_size = int(input("Nhập kích thước quần thể: "))
num_generations = int(input("Nhập số thế hệ: "))
mutation_rate = float(input("Nhập tỷ lệ đột biến (0.0 - 1.0): "))
num_operations = int(input("Nhập số lượng thao tác: "))

operations = []
for i in range(num_operations):
    operation_duration = int(input(f"Nhập thời gian chạy máy cho thao tác {i + 1}: "))
    operations.append(operation_duration)

def create_population(operations, population_size):
    return [random.sample(operations, len(operations)) for _ in range(population_size)]

def fitness(individual):
    return sum(individual)

def selection(population):
    sorted_population = sorted(population, key=fitness)
    return sorted_population[:len(population) // 2]

def crossover(parent1, parent2):
    child1 = [None] * len(parent1)
    child2 = [None] * len(parent2)
    start, end = sorted(random.sample(range(len(parent1)), 2))

    for i in range(start, end + 1):
        child1[i] = parent1[i]
        child2[i] = parent2[i]

    remaining1 = [op for op in parent2 if op not in child1[start:end + 1]]
    remaining2 = [op for op in parent1 if op not in child2[start:end + 1]]

    for i in range(len(child1)):
        if child1[i] is None:
            child1[i] = remaining1.pop(0)
        if child2[i] is None:
            child2[i] = remaining2.pop(0)

    return child1, child2


def mutation(individual, mutation_rate):
    mutated_individual = individual[:]
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            swap_index = random.randint(0, len(mutated_individual) - 1)
            mutated_individual[i], mutated_individual[swap_index] = mutated_individual[swap_index], mutated_individual[i]
    return mutated_individual

def genetic_algorithm(operations, population_size, num_generations, mutation_rate):
    if population_size < 2:
        raise ValueError("Population size must be at least 2")

    population = create_population(operations, population_size)
    best_individual = min(population, key=fitness)
    print("Generation 0 - Best individual fitness:", fitness(best_individual))

    for generation in range(1, num_generations + 1):
        selected_individuals = selection(population)

        offspring = []
        while len(offspring) < population_size:
            parents = random.sample(selected_individuals, 2)
            child1, child2 = crossover(parents[0], parents[1])
            offspring.extend([child1, child2])

        offspring = offspring[:population_size]
        population = [mutation(individual, mutation_rate) for individual in offspring]

        current_best = min(population, key=fitness)
        if fitness(current_best) < fitness(best_individual):
            best_individual = current_best

        print(f"Generation {generation} - Best individual fitness:", fitness(best_individual))

    return best_individual

#Chạy
result = genetic_algorithm(operations, population_size, num_generations, mutation_rate)
print(f"Lịch trình tối ưu: {result}")
print(f"Tổng thời gian chạy máy: {sum(result)}")
