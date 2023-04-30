def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def input_graph():
    n = int(input("Nhập số lượng đỉnh: "))
    graph = {}
    print("Nhập danh sách kề cho mỗi đỉnh:")
    for i in range(n):
        vertex, neighbors = input().split(':')
        graph[vertex] = neighbors.split() if neighbors else []
    return graph

def main():
    graph = input_graph()
    start_vertex = input("Nhập đỉnh bắt đầu: ")
    visited = dfs(graph, start_vertex)
    print(f"Các đỉnh đã duyệt theo DFS: {visited}")

if __name__ == "__main__":
    main()
