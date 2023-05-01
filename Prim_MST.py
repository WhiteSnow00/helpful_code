import sys
from heapq import heappush, heappop

def prim(graph, start):
    visited = set()
    min_heap = []
    total_cost = 0
    mst_edges = []

    visited.add(start)
    for edge in graph[start]:
        heappush(min_heap, edge)

    while min_heap:
        cost, u, v = heappop(min_heap)

        if v not in visited:
            visited.add(v)
            total_cost += cost
            mst_edges.append((u, v))

            for edge in graph[v]:
                if edge[2] not in visited:
                    heappush(min_heap, edge)

    return total_cost, mst_edges

def main():
    print("Enter the number of nodes and edges:")
    nodes, edges = map(int, input().split())

    graph = {i: [] for i in range(1, nodes + 1)}

    print("Enter the edges and their weights:")
    for _ in range(edges):
        u, v, weight = map(int, input().split())
        graph[u].append((weight, u, v))
        graph[v].append((weight, v, u))

    start = 1
    cost, mst = prim(graph, start)
    print("Total cost:", cost)
    print("Minimum Spanning Tree edges:")
    for edge in mst:
        print(f"{edge[0]} - {edge[1]}")

if __name__ == "__main__":
    main()
