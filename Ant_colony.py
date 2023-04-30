import numpy as np
import random

def distance(city1, city2):
    return np.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def calculate_distances(cities):
    n_cities = len(cities)
    distances = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            dist = distance(cities[i], cities[j])
            distances[i][j] = dist
            distances[j][i] = dist
    return distances

def ant_colony_optimization(cities, n_ants, n_iterations, alpha=1, beta=5, rho=0.5, q=100):
    n_cities = len(cities)
    distances = calculate_distances(cities)
    pheromones = np.ones((n_cities, n_cities))

    best_path = None
    best_path_length = np.inf

    for _ in range(n_iterations):
        paths = []
        for ant in range(n_ants):
            path = [random.randint(0, n_cities - 1)]
            available_cities = list(range(n_cities))
            available_cities.remove(path[0])

            for _ in range(n_cities - 1):
                p = np.zeros(len(available_cities))
                for i, city in enumerate(available_cities):
                    p[i] = (pheromones[path[-1]][city]**alpha) * (1/distances[path[-1]][city])**beta
                p /= p.sum()

                next_city = np.random.choice(available_cities, p=p)
                path.append(next_city)
                available_cities.remove(next_city)

            path_length = sum(distances[path[i]][path[i + 1]] for i in range(n_cities - 1))
            path_length += distances[path[-1]][path[0]]

            if path_length < best_path_length:
                best_path_length = path_length
                best_path = path

            paths.append(path)

        for path in paths:
            for i in range(n_cities - 1):
                pheromones[path[i]][path[i + 1]] += q / distances[path[i]][path[i + 1]]
                pheromones[path[i + 1]][path[i]] += q / distances[path[i]][path[i + 1]]
            pheromones[path[-1]][path[0]] += q / distances[path[-1]][path[0]]
            pheromones[path[0]][path[-1]] += q / distances[path[-1]][path[0]]

        pheromones *= (1 - rho)

    return best_path, best_path_length

def input_distance_matrix():
    n = int(input("Nhập số lượng thành phố: "))
    cities = []
    print("Nhập tọa độ thành phố:")
    for i in range(n):
        row = list(map(float, input().split()))
        cities.append(row)
    return cities

def main():
    cities = input_distance_matrix()

    n_ants = 10
    n_iterations = 100
    best_path, best_cost = ant_colony_optimization(cities, n_ants, n_iterations)
    print(f"Đường đi tối ưu: {best_path}")
    print(f"Tổng chi phí tối thiểu: {best_cost}")

if __name__ == "__main__":
    main()
