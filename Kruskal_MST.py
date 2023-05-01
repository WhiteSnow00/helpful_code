def find(parent, node):
    if parent[node] == node:
        return node
    parent[node] = find(parent, parent[node])
    return parent[node]

def union(parent, rank, node1, node2):
    root1 = find(parent, node1)
    root2 = find(parent, node2)

    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]:
                rank[root2] += 1

def kruskal(edges, nodes):
    edges.sort(key=lambda edge: edge[2])

    parent = {node: node for node in range(1, nodes + 1)}
    rank = {node: 0 for node in range(1, nodes + 1)}

    mst_edges = []
    total_cost = 0

    for edge in edges:
        u, v, weight = edge
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_edges.append((u, v))
            total_cost += weight

    return total_cost, mst_edges

def main():
    print("Enter the number of nodes and edges:")
    nodes, edges_count = map(int, input().split())

    edges = []

    print("Enter the edges and their weights:")
    for _ in range(edges_count):
        u, v, weight = map(int, input().split())
        edges.append((u, v, weight))

    cost, mst = kruskal(edges, nodes)
    print("Total cost:", cost)
    print("Minimum Spanning Tree edges:")
    for edge in mst:
        print(f"{edge[0]} - {edge[1]}")

if __name__ == "__main__":
    main()
