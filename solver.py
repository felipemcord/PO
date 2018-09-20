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

def CreateRestrictions(InputFile, VariableNumber, RestrictionNumber, FreeVariables, Objective):
    Restrictions = []
    B = []
    FPIVariables = 0
    for i in range(RestrictionNumber):
        Line = InputFile.readline().split()

        Restriction = [0]
        for Variable in range(VariableNumber):
            if(Variable in FreeVariables):
                Restriction.extend([float(Line[Variable] ),-float(Line[Variable])])
            else:
                Restriction.append(float(Line[Variable]))

        for Variable in range(FPIVariables):
            Restriction.append(0)
        
        if(Line[VariableNumber] == ">="):
            Restriction.append(-1)
            Objective.append(0)
            FPIVariables += 1
            for Array in Restrictions:
                Array.append(0)
        elif(Line[VariableNumber] == "<="):
            Restriction.append(1)
            FPIVariables += 1
            Objective.append(0)
            for Array in Restrictions:
                Array.append(0)

        Restrictions.append(Restriction)
        B.append(float(Line[-1]))
        
    for Index,Restriction in enumerate(Restrictions):
        Restriction.append(B[Index])

    return Restrictions
        

def CreateInputArray(file):
    
    InputFile = open(file,'r')
    VariableNumber = int(InputFile.readline())
    RestrictionNumber = int(InputFile.readline())
    
    FreeVariables = []
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        if(int(Value) != 1):
            FreeVariables.append(Variable)
    
    Objective = [1]
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        if(Variable in FreeVariables):
            Objective.extend([float(Value),-float(Value)])
        else:
            Objective.append(float(Value))
    Restrictions = CreateRestrictions(InputFile, VariableNumber, RestrictionNumber, FreeVariables, Objective)
    Objective.append(0)
    A = [Objective]
    A.extend(Restrictions)
    for Line in A:
        print(Line)
    # print(A)
    return A

CreateInputArray('exercicio9a.txt')
# I = np.identity(4)
# A = np.arange(20).reshape(4, 5) ** 2
# print(A)
# print(A[1,range(1,A.shape[1] )])
# Canon(A)