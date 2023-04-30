def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(x.bit_length(), y.bit_length())
    m = n // 2

    mask = (1 << m) - 1
    low1, low2 = x & mask, y & mask
    high1, high2 = x >> m, y >> m

    z0 = karatsuba(low1, low2)
    z1 = karatsuba(low1 ^ high1, low2 ^ high2)
    z2 = karatsuba(high1, high2)

    return (z2 << (2 * m)) + ((z1 ^ z2 ^ z0) << m) + z0

if __name__ == "__main__":
    num1 = int(input("Nhap so thu nhat: "))
    num2 = int(input("Nhap so thu hai: "))
    result = karatsuba(num1, num2)
    print(f"Ket qua phep nhan {num1} va {num2} la: {result}.")
