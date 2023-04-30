import sys
from heapq import heappop, heappush

def dijkstra(graph, start):
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(priority_queue, (distance, neighbor))

    return distances

if __name__ == "__main__":
    print("Enter the number of vertices:")
    num_vertices = int(input())

    print("Enter the number of edges:")
    num_edges = int(input())

    graph = {}

    print("Enter edges (format: source_vertex destination_vertex weight):")
    for _ in range(num_edges):
        src, dest, weight = map(int, input().split())
        if src not in graph:
            graph[src] = {}
        if dest not in graph:
            graph[dest] = {}

        graph[src][dest] = weight
        graph[dest][src] = weight

    print("Enter the starting vertex:")
    start_vertex = int(input())

    shortest_paths = dijkstra(graph, start_vertex)

    print("Shortest path distances from vertex", start_vertex, ":")
    for vertex, distance in shortest_paths.items():
        print(f"{vertex}: {distance}")
