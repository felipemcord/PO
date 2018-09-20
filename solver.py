import numpy as np

def removeSmallNumbers(A):
    A[abs(A) < 10**(-10)] = 0
    return A

def Pivot(A , i, j):
    E = np.identity(A.shape[0])
    print(i,j)
    if(A[i,j] != 1):
        E[i,...] /= A[i,j]
    for row in range(A.shape[0]):
        if(A[row,j] != 0 and row != i):
            E[row,i] = -(A[row,j]/A[i,j])
    A = removeSmallNumbers(E.dot(A))
    print(A)
    print("\n")
    print(E)
    print("\n\n")
    return A

def Canon( A ):
    firstLine = A[0]
    pivotLines = []
    for i in list(reversed(range(firstLine.shape[0] - 1))):
        column = A[...,i]
        for j in range(1,column.shape[0]):
            if(column[j] != 0 and j not in pivotLines):
                A = Pivot(A,j,i)
                pivotLines.append(j)
                break
    return A

I = np.identity(4)
A = np.arange(20).reshape(4, 5) ** 2
print(A)
print("\n\n")
Canon(A)