def display(n, a):
    for i in range(1, n+1):
        print(f"Con hau o hang thu {i} nam o cot {a[i]}")

def Try(i, n, a, cot, d1, d2):
    for j in range(1, n+1):
        if cot[j] == 1 and d1[i - j + n] == 1 and d2[i + j - 1] == 1:
            a[i] = j
            cot[j] = d1[i - j + n] = d2[i + j - 1] = 0
            if i == n:
                display(n, a)
            else:
                Try(i + 1, n, a, cot, d1, d2)
            cot[j] = d1[i - j + n] = d2[i + j - 1] = 1

def main():
    n = int(input("Nhap n = "))
    a = [0] * (n + 1)
    cot = [1] * (2 * n + 1)
    d1 = [1] * (2 * n + 1)
    d2 = [1] * (2 * n + 1)
    Try(1, n, a, cot, d1, d2)

if __name__ == "__main__":
    main()
