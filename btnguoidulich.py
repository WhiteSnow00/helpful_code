import sys
from itertools import permutations

def tsp(cities, distance_matrix):
    n = len(cities)
    min_path = None
    min_cost = sys.maxsize

    for perm in permutations(cities[1:]):
        path = [cities[0]] + list(perm) + [cities[0]]
        cost = path_cost(path, distance_matrix)
        if cost < min_cost:
            min_cost = cost
            min_path = path

    return min_path, min_cost

def path_cost(path, distance_matrix):
    cost = 0
    for i in range(len(path) - 1):
        cost += distance_matrix[path[i]][path[i + 1]]
    return cost

def input_distance_matrix():
    n = int(input("Nhập số lượng thành phố: "))
    distance_matrix = []
    print("Nhập ma trận khoảng cách:")
    for i in range(n):
        row = list(map(int, input().split()))
        distance_matrix.append(row)
    return distance_matrix

def main():
    distance_matrix = input_distance_matrix()
    cities = list(range(len(distance_matrix)))

    min_path, min_cost = tsp(cities, distance_matrix)
    print(f"Đường đi tối ưu: {min_path}")
    print(f"Tổng chi phí tối thiểu: {min_cost}")

if __name__ == "__main__":
    main()
