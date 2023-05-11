STDIN.set_encoding(Encoding::UTF_8)
STDOUT.set_encoding(Encoding::UTF_8)
# Import the necessary library
require 'securerandom'

# User input
puts "Nhap kich thuoc quan the: "
population_size = gets.chomp.to_i
puts "Nhap so the he: "
num_generations = gets.chomp.to_i
puts "Nhap ti le dot bien (0.0-1.0): "
mutation_rate = gets.chomp.to_f
puts "Nhap so luong thao tac: "
num_operations = gets.chomp.to_i

operations = []
(1..num_operations).each do |i|
    puts "Nhap thoi gian chay may cho thao tac #{i}: "
    operation_duration = gets.chomp.to_i
    operations.append(operation_duration)
end

def create_population(operations, population_size)
    population = []
    population_size.times do
        population.append(operations.shuffle)
    end
    return population
end

def fitness(individual)
    return individual.sum
end

def selection(population)
    sorted_population = population.sort_by {|individual| fitness(individual)}
    return sorted_population[0, population.size / 2]
end

def crossover(parent1, parent2)
    child1 = Array.new(parent1.size)
    child2 = Array.new(parent2.size)
    start, stop = [SecureRandom.random_number(parent1.size), SecureRandom.random_number(parent1.size)].sort

    (start..stop).each do |i|
        child1[i] = parent1[i]
        child2[i] = parent2[i]
    end

    remaining1 = parent2.reject {|gene| child1.include?(gene)}
    remaining2 = parent1.reject {|gene| child2.include?(gene)}

    child1.each_with_index do |gene, i|
        next if start <= i && i <= stop
        if remaining1.size > 0
            child1[i] = remaining1.shift
        else
            child1[i] = remaining2.shift
        end
    end

    child2.each_with_index do |gene, i|
        next if start <= i && i <= stop
        if remaining2.size > 0
            child2[i] = remaining2.shift
        else
            child2[i] = remaining1.shift
        end
    end

    return child1, child2
end

def mutation(individual, mutation_rate)
    mutated_individual = individual.dup
    mutated_individual.each_with_index do |gene, i|
        if SecureRandom.random_number < mutation_rate
            swap_index = SecureRandom.random_number(mutated_individual.size)
            mutated_individual[i], mutated_individual[swap_index] = mutated_individual[swap_index], mutated_individual[i]
        end
    end
    return mutated_individual
end

def genetic_algorithm(operations, population_size, num_generations, mutation_rate)
    if population_size < 2
        raise "Population size must be at least 2"
    end

    population = create_population(operations, population_size)
    best_individual = population.min_by {|individual| fitness(individual)}
    puts "Generation 0 - Best individual fitness: #{fitness(best_individual)}"

    (1..num_generations).each do |generation|
        selected_individuals = selection(population)

        offspring = []
        while offspring.size < population_size
            parents = selected_individuals.sample(2)
            child1, child2 = crossover(parents[0], parents[1])
            offspring.concat([child1, child2])
        end

        offspring = offspring[0, population_size]
        population = offspring.map {|individual| mutation(individual, mutation_rate)}

        current_best = population.min_by {|individual| fitness(individual)}
        if fitness(current_best) < fitness(best_individual)
            best_individual = current_best
        end

        puts "Generation #{generation} - Best individual fitness: #{fitness(best_individual)}"
    end

    return best_individual
end

# Run the algorithm
result = genetic_algorithm(operations, population_size, num_generations, mutation_rate)
puts "Lich trinh toi uu: #{result}"
puts "Tong thoi gian chay may: #{result.sum}"