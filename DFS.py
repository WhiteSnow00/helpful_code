from collections import defaultdict

def dfs_recursive(graph, start, visited=None, order=None):
    """DFS traversal (recursive) returning vertices in visit order."""
    if visited is None:
        visited = set()
        order = []
    
    visited.add(start)
    order.append(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)
    
    return order

def dfs_iterative(graph, start):
    """DFS traversal (iterative) using stack."""
    visited = set()
    stack = [start]
    order = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            # Add neighbors in reverse order to maintain left-to-right traversal
            stack.extend(reversed(graph[vertex]))
    
    return order

def dfs_path(graph, start, end, path=None, visited=None):
    """Find a path between two vertices using DFS."""
    if path is None:
        path = []
        visited = set()
    
    path.append(start)
    visited.add(start)
    
    if start == end:
        return path
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs_path(graph, neighbor, end, path, visited)
            if result:
                return result
    
    path.pop()
    return None

def has_cycle(graph, start, visited=None, parent=None):
    """Detect cycle in undirected graph using DFS."""
    if visited is None:
        visited = set()
    
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            if has_cycle(graph, neighbor, visited, start):
                return True
        elif parent != neighbor:
            return True
    
    return False

def topological_sort(graph):
    """Topological sort using DFS (for directed graphs)."""
    visited = set()
    stack = []
    
    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)
    
    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)
    
    return stack[::-1]

def connected_components(graph):
    """Find all connected components using DFS."""
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = dfs_recursive(graph, vertex)
            components.append(component)
            visited.update(component)
    
    return components

def input_graph():
    n = int(input("Number of vertices: "))
    m = int(input("Number of edges: "))
    
    graph = defaultdict(list)
    print("Enter edges (u v):")
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)  # For undirected graph
    
    return graph

def main():
    graph = input_graph()
    
    print("\n1. DFS Traversal (Recursive)")
    print("2. DFS Traversal (Iterative)")
    print("3. Find Path")
    print("4. Detect Cycle")
    print("5. Connected Components")
    
    choice = int(input("\nChoice: "))
    
    if choice == 1:
        start = int(input("Start vertex: "))
        result = dfs_recursive(graph, start)
        print(f"DFS order (recursive): {result}")
        
    elif choice == 2:
        start = int(input("Start vertex: "))
        result = dfs_iterative(graph, start)
        print(f"DFS order (iterative): {result}")
        
    elif choice == 3:
        start = int(input("Start vertex: "))
        end = int(input("End vertex: "))
        path = dfs_path(graph, start, end)
        if path:
            print(f"Path: {' -> '.join(map(str, path))}")
        else:
            print("No path exists")
            
    elif choice == 4:
        start = int(input("Start vertex: "))
        if has_cycle(graph, start):
            print("Graph contains a cycle")
        else:
            print("Graph is acyclic")
            
    elif choice == 5:
        components = connected_components(graph)
        print(f"Found {len(components)} component(s):")
        for i, component in enumerate(components, 1):
            print(f"Component {i}: {component}")

if __name__ == "__main__":
    main()
