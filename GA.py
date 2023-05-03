import random
import numpy as np

# Đầu vào
population_size = int(input("Nhập kích thước quần thể: "))
num_generations = int(input("Nhập số thế hệ: "))
mutation_rate = float(input("Nhập tỷ lệ đột biến (0.0 - 1.0): "))
num_operations = int(input("Nhập số lượng thao tác: "))

operations = []
for i in range(num_operations):
    operation_duration = int(input(f"Nhập thời gian chạy máy cho thao tác {i + 1}: "))
    operations.append(operation_duration)

def create_individual(operations):
    return random.sample(operations, len(operations))

def create_population(operations, population_size):
    return [create_individual(operations) for _ in range(population_size)]

def fitness(individual):
    return sum(individual)

def selection(population):
    sorted_population = sorted(population, key=fitness)
    return sorted_population[:len(population) // 2]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def crossover_population(selected_individuals):
    offspring = []
    while len(offspring) < len(selected_individuals):
        parent1 = random.choice(selected_individuals)
        parent2 = random.choice(selected_individuals)
        if parent1 != parent2:
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)
    return offspring[:len(selected_individuals)]

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            swap_index = random.randint(0, len(individual) - 1)
            individual[i], individual[swap_index] = individual[swap_index], individual[i]
    return individual

def genetic_algorithm(operations, population_size, num_generations, mutation_rate):
    if population_size < 2:
        raise ValueError("Population size must be at least 2")

    population = [random.sample(operations, len(operations)) for _ in range(population_size)]
    best_individual = min(population, key=fitness)
    print("Generation 0 - Best individual fitness:", fitness(best_individual))

    for generation in range(1, num_generations + 1):
        selected_individuals = [selection(population) for _ in range(population_size // 2)]

        offspring = []
        while len(offspring) < population_size:
            parent1 = random.choice(selected_individuals)
            if len(selected_individuals) == 1:
                child1, child2 = parent1, parent1
            else:
                parent2 = random.choice([ind for ind in selected_individuals if ind != parent1])
                child1, child2 = crossover(parent1, parent2)

            offspring.append(child1)
            offspring.append(child2)

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

