def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_element = max(arr)
    exp = 1
    while max_element // exp > 0:
        counting_sort(arr, exp)
        exp *= 10


def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high and target >= arr[low] and target <= arr[high]:
        index = low + int(((float(target - arr[low]) * (high - low)) / (arr[high] - arr[low])))
        if arr[index] == target:
            return index
        elif arr[index] < target:
            low = index + 1
        else:
            high = index - 1

    return -1


def input_array():
    arr = list(map(int, input("Nhập dãy số ngăn cách nhau bới dấu cách: ").split()))
    return arr


def main():
    arr = input_array()
    radix_sort(arr)
    target = int(input("Nhập số cần tìm: "))

    result = interpolation_search(arr, target)
    if result != -1:
        print(f"Số {target} được tìm thấy ở vị trí {result}")
    else:
        print("Không tìm thấy")


if __name__ == "__main__":
    main()
