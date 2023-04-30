def generation(n, a):
    i = n - 1
    while i >= 0 and a[i] > a[i + 1]:
        i -= 1

    if i == -1:
        return False

    j = n
    while a[i] > a[j]:
        j -= 1

    a[i], a[j] = a[j], a[i]

    l, r = i + 1, n
    while l < r:
        a[l], a[r] = a[r], a[l]
        l += 1
        r -= 1

    return True


def main():
    n = int(input("Nhap n: "))
    a = list(range(1, n + 1))
    element_last = True

    while element_last:
        print("".join(str(x) for x in a))
        element_last = generation(n - 1, a)


if __name__ == "__main__":
    main()
