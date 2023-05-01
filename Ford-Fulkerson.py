from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def dfs(self, source, sink, parent, visited):
        visited[source] = True

        if source == sink:
            return True

        for neighbor in self.graph[source]:
            if not visited.get(neighbor, False) and self.graph[source][neighbor] > 0:
                parent[neighbor] = source
                if self.dfs(neighbor, sink, parent, visited):
                    return True

        return False


    def ford_fulkerson(self, source, sink):
        parent = {node: -1 for node in self.graph}
        visited = {node: False for node in self.graph}

        max_flow = 0

        while self.dfs(source, sink, parent, visited):
            path_flow = float('Inf')

            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = parent[v]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            visited = {node: False for node in self.graph}

        return max_flow


def main():
    print("Enter the number of nodes and edges:")
    nodes, edges_count = map(int, input().split())

    graph = Graph(nodes)

    print("Enter the edges and their capacities:")
    for _ in range(edges_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u, v, capacity)

    print("Enter the source and sink nodes:")
    source, sink = map(int, input().split())

    max_flow = graph.ford_fulkerson(source, sink)
    print("Maximum flow:", max_flow)

if __name__ == "__main__":
    main()
