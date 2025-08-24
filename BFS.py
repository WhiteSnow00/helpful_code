from collections import defaultdict, deque

def bfs(graph, start):
    """BFS traversal returning vertices in visit order."""
    visited = set([start])
    queue = deque([start])
    order = []
    
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return order

def bfs_shortest_path(graph, start, end):
    """Find shortest path between two vertices."""
    if start == end:
        return [start]
    
    visited = set([start])
    queue = deque([(start, [start])])
    
    while queue:
        vertex, path = queue.popleft()
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    
    return None

def bfs_distance(graph, start):
    """Get distance of all vertices from start vertex."""
    visited = set([start])
    queue = deque([(start, 0)])
    distances = {start: 0}
    
    while queue:
        vertex, dist = queue.popleft()
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))
    
    return distances

def input_graph():
    n = int(input("Number of vertices: "))
    m = int(input("Number of edges: "))
    
    graph = defaultdict(list)
    print("Enter edges (u v):")
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    return graph

def main():
    graph = input_graph()
    
    print("\n1. BFS Traversal")
    print("2. Shortest Path")
    print("3. Distance from vertex")
    
    choice = int(input("\nChoice: "))
    
    if choice == 1:
        start = int(input("Start vertex: "))
        result = bfs(graph, start)
        print(f"BFS order: {result}")
        
    elif choice == 2:
        start = int(input("Start vertex: "))
        end = int(input("End vertex: "))
        path = bfs_shortest_path(graph, start, end)
        if path:
            print(f"Path: {' -> '.join(map(str, path))}")
        else:
            print("No path exists")
            
    elif choice == 3:
        start = int(input("Start vertex: "))
        distances = bfs_distance(graph, start)
        for vertex, dist in sorted(distances.items()):
            print(f"Vertex {vertex}: distance {dist}")

if __name__ == "__main__":
    main()
