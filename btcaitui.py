def Nhap():
    global n, W, c, a
    n = int(input("Nhap so luong do vat: "))
    W = int(input("Nhap khoi luong do vat: "))
    c = [0] * (n + 1)
    a = [0] * (n + 1)

    for i in range(1, n + 1):
        c[i] = int(input(f"Nhap vao so cong dung cua do vat {i}: "))

    for i in range(1, n + 1):
        a[i] = int(input(f"Nhap khoi luong do vat thu {i}: "))

def xuat(f):
    print("________BANG TINH____________")
    for i in range(1, n + 1):
        for j in range(W + 1):
            print(f[i][j], end=" ")
        print()

def max(a, b):
    return a if a > b else b

def BPA():
    f = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        f[i][0] = 0

    for j in range(W + 1):
        f[0][j] = 0

    for i in range(1, n + 1):
        for j in range(W + 1):
            if a[i] <= j:
                f[i][j] = max(f[i - 1][j], f[i - 1][j - a[i]] + c[i])
            else:
                f[i][j] = f[i - 1][j]
    
    return f

def Truyvet(f):
    i = n
    j = W
    GT = 0
    items = []

    while i != 0 and j != 0:
        if f[i][j] != f[i - 1][j]:
            items.append(i)
            GT += c[i]
            j -= a[i]
        i -= 1
    
    return items, GT

def main():
    Nhap()
    print("________CAC GIA TRI SAU KHI NHAP_________")
    print(f"Trong luong gioi han cua tui la: {W}")
    print("Trong luong do vat:")
    for i in range(1, n + 1):
        print(c[i], end=" ")
    print("\nGia tri cua do vat:")
    for i in range(1, n + 1):
        print(a[i], end=" ")
    print()

    f = BPA()
    xuat(f)

    items, GT = Truyvet(f)
    print(f"\n\nCac do vat duoc cho vao tui la: {items}")
    print(f"\n\nTong gia tri toi da cua tui la: {W}")
    print(f"\n\nTong gia trong luong cua do vat duoc vao tui la: {GT}")

if __name__ == "__main__":
    main()
