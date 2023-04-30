def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def strassen(A, B):
    if len(A) == 1:
        return [[A[0][0] * B[0][0]]]

    mid = len(A) // 2
    A11, A12, A21, A22 = A[:mid], [row[mid:] for row in A[:mid]], A[mid:], [row[mid:] for row in A[mid:]]
    B11, B12, B21, B22 = B[:mid], [row[mid:] for row in B[:mid]], B[mid:], [row[mid:] for row in B[mid:]]

    P1 = strassen(A11, subtract_matrices(B12, B22))
    P2 = strassen(add_matrices(A11, A12), B22)
    P3 = strassen(add_matrices(A21, A22), B11)
    P4 = strassen(A22, subtract_matrices(B21, B11))
    P5 = strassen(add_matrices(A11, A22), add_matrices(B11, B22))
    P6 = strassen(subtract_matrices(A12, A22), add_matrices(B21, B22))
    P7 = strassen(subtract_matrices(A11, A21), add_matrices(B11, B12))

    C11 = add_matrices(subtract_matrices(add_matrices(P5, P4), P2), P6)
    C12 = add_matrices(P1, P2)
    C21 = add_matrices(P3, P4)
    C22 = subtract_matrices(subtract_matrices(add_matrices(P5, P1), P3), P7)

    return [row1 + row2 for row1, row2 in zip(C11, C12)] + [row1 + row2 for row1, row2 in zip(C21, C22)]


if __name__ == "__main__":
    print("Nhập size ma trận (phải là lũy thừa của 2):")
    size = int(input())

    print("Nhap ma tran 1:")
    A = [list(map(int, input().split())) for _ in range(size)]

    print("Nhap ma tran 2:")
    B = [list(map(int, input().split())) for _ in range(size)]

    product = strassen(A, B)

    print("Ket qua:")
    for row in product:
        print(*row)
