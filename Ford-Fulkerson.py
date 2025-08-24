from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.original = defaultdict(lambda: defaultdict(int))
    
    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.original[u][v] = capacity
    
    def bfs(self, source, sink, parent):
        """BFS to find augmenting path (Edmonds-Karp improvement)."""
        visited = set([source])
        queue = deque([source])
        
        while queue:
            u = queue.popleft()
            
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        
        return False
    
    def dfs(self, source, sink, parent):
        """DFS to find augmenting path."""
        visited = set()
        stack = [source]
        
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            
            if u == sink:
                return True
            
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    parent[v] = u
                    stack.append(v)
        
        return False
    
    def ford_fulkerson(self, source, sink, use_bfs=True):
        """Find maximum flow using Ford-Fulkerson algorithm."""
        parent = {}
        max_flow = 0
        paths = []
        
        find_path = self.bfs if use_bfs else self.dfs
        
        while find_path(source, sink, parent):
            # Find minimum capacity along the path
            path_flow = float('inf')
            path = []
            v = sink
            
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                path.append(v)
                v = u
            path.append(source)
            path.reverse()
            
            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u
            
            max_flow += path_flow
            paths.append((path, path_flow))
            parent.clear()
        
        return max_flow, paths
    
    def min_cut(self, source):
        """Find minimum cut after running max flow."""
        visited = set()
        queue = deque([source])
        visited.add(source)
        
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    queue.append(v)
        
        cut_edges = []
        for u in visited:
            for v in self.original[u]:
                if v not in visited and self.original[u][v] > 0:
                    cut_edges.append((u, v, self.original[u][v]))
        
        return cut_edges, visited
    
    def reset(self):
        """Reset graph to original capacities."""
        self.graph = defaultdict(lambda: defaultdict(int))
        for u in self.original:
            for v in self.original[u]:
                self.graph[u][v] = self.original[u][v]

def input_graph():
    n = int(input("Number of vertices: "))
    m = int(input("Number of edges: "))
    
    graph = Graph()
    print("Enter edges (u v capacity):")
    for _ in range(m):
        u, v, cap = map(int, input().split())
        graph.add_edge(u, v, cap)
    
    return graph

def main():
    graph = input_graph()
    
    print("\n1. Ford-Fulkerson with DFS")
    print("2. Edmonds-Karp (Ford-Fulkerson with BFS)")
    print("3. Find Minimum Cut")
    print("4. Show Augmenting Paths")
    
    choice = int(input("\nChoice: "))
    
    source = int(input("Source vertex: "))
    sink = int(input("Sink vertex: "))
    
    if choice == 1:
        graph.reset()
        max_flow, paths = graph.ford_fulkerson(source, sink, use_bfs=False)
        print(f"Maximum flow (DFS): {max_flow}")
        
    elif choice == 2:
        graph.reset()
        max_flow, paths = graph.ford_fulkerson(source, sink, use_bfs=True)
        print(f"Maximum flow (BFS): {max_flow}")
        
    elif choice == 3:
        graph.reset()
        max_flow, _ = graph.ford_fulkerson(source, sink)
        cut_edges, s_side = graph.min_cut(source)
        print(f"Maximum flow: {max_flow}")
        print(f"Minimum cut edges:")
        for u, v, cap in cut_edges:
            print(f"  {u} -> {v} (capacity: {cap})")
        print(f"S-side vertices: {sorted(s_side)}")
        
    elif choice == 4:
        graph.reset()
        max_flow, paths = graph.ford_fulkerson(source, sink)
        print(f"Maximum flow: {max_flow}")
        print(f"Augmenting paths:")
        for i, (path, flow) in enumerate(paths, 1):
            path_str = ' -> '.join(map(str, path))
            print(f"  Path {i}: {path_str} (flow: {flow})")

if __name__ == "__main__":
    main()
