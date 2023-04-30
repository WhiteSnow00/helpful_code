from collections import defaultdict, deque

def bfs(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)

    return visited

def input_graph():
    n = int(input("Enter the number of vertices: "))
    m = int(input("Enter the number of edges: "))

    graph = defaultdict(list)
    print("Enter the edges (as vertex pairs):")
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    return graph

def main():
    graph = input_graph()
    start_vertex = int(input("Enter the starting vertex: "))
    visited_vertices = bfs(graph, start_vertex)
    print(f"Vertices visited in BFS order: {visited_vertices}")

if __name__ == "__main__":
    main()
