def bellman_ford(graph, source):
    distance, predecessor = {}, {}
    
    for vertex in graph:
        distance[vertex] = float("inf")
        predecessor[vertex] = None
        
    distance[source] = 0
    
    for _ in range(len(graph) - 1):
        for vertex in graph:
            for neighbor, weight in graph[vertex]:
                if distance[vertex] + weight < distance[neighbor]:
                    distance[neighbor] = distance[vertex] + weight
                    predecessor[neighbor] = vertex

    for vertex in graph:
        for neighbor, weight in graph[vertex]:
            if distance[vertex] + weight < distance[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    return distance, predecessor


if __name__ == "__main__":
    vertices = int(input("Enter the number of vertices: "))
    edges = int(input("Enter the number of edges: "))

    graph = {vertex: [] for vertex in range(1, vertices + 1)}

    for _ in range(edges):
        u, v, w = map(int, input("Enter edge (u, v, w): ").split())
        graph[u].append((v, w))

    source_vertex = int(input("Enter the source vertex: "))
    
    dist, pred = bellman_ford(graph, source_vertex)

    print("Shortest Path:")
    for vertex in graph:
        print(f"Vertex {vertex}, Distance: {dist[vertex]}, Predecessor: {pred[vertex]}")
