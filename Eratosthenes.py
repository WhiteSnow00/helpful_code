def sieve_of_eratosthenes(n):
    prime = [True] * (n + 1)
    prime[0], prime[1] = False, False
    p = 2
    while p**2 <= n:
        if prime[p]:
            for i in range(p**2, n + 1, p):
                prime[i] = False
        p += 1

    return [i for i in range(2, n + 1) if prime[i]]

def main():
    n = int(input("Nhập giá trị của n: "))
    prime_numbers = sieve_of_eratosthenes(n)
    print(f"Các số nguyên tố từ 1 đến {n}: {prime_numbers}")

if __name__ == "__main__":
    main()
