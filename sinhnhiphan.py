def generation(n, a):
    i = n - 1
    while i >= 0 and a[i] == 1:
        a[i] = 0
        i -= 1
    if i == -1:
        return False
    else:
        a[i] = 1
        return True

if __name__ == "__main__":
    n = int(input("n = "))
    a = [0] * n
    element_last = True
    while element_last:
        print("".join(map(str, a)))
        element_last = generation(n, a)
