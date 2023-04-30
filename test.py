from collections import defaultdict

def eulerian_path(adj):
    odd_degree_count = 0
    start_vertex = 0

    n = len(adj)

    for i in range(n):
        if len(adj[i]) % 2 == 1:
            odd_degree_count += 1
            start_vertex = i

    if odd_degree_count != 0 and odd_degree_count != 2:
        return []

    cur_path = [start_vertex]
    euler_path = []

    while cur_path:
        u = cur_path[-1]

        if not adj[u]:
            euler_path.append(u)
            cur_path.pop()
        else:
            v = adj[u].pop()
            cur_path.append(v)
            adj[v].discard(u)

    return euler_path

def main():
    n = int(input("Nhap so dinh: "))
    m = int(input("Nhap so canh: "))
    adj = defaultdict(set)
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].add(v)
        adj[v].add(u)

    res = eulerian_path(adj)
    print(" ".join(str(i) for i in res))

if __name__ == "__main__":
    main()
