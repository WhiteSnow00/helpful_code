def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x

def find_solution(a, b):
    gcd, x, y = extended_euclidean(a, b)
    return gcd, x, y

def main():
    a = int(input("Nhập a: "))
    b = int(input("Nhập b: "))

    gcd, x, y = find_solution(a, b)
    print("gcd:", gcd)
    print("x:", x)
    print("y:", y)

if __name__ == "__main__":
    main()
