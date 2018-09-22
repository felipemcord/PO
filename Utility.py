import numpy as np
import LPs

def removeSmallNumbers(A):
    A[abs(A) < 10**(-10)] = 0
    return A

def insertValueinMatrix(PL,value,pos):
    A = np.zeros((PL.A.shape[0],PL.A.shape[1] + 1))
    for i in range(PL.A.shape[0]):
        A[i] = np.insert(PL.A[i],pos,value)
    PL.A = A

def MakeIdentity(PL):
    Line = 1
    while Line < PL.RestrictionNumber:
        pivotLine = Line + np.argmin(PL.pivotColumns[Line:])
        if pivotLine != Line:
            SwitchLines(PL,pivotLine,Line)
            PL.pivotColumns[pivotLine] =  PL.pivotColumns[Line]
            PL.pivotColumns[Line] = Line
        Line += 1
        

def SwitchLines(PL,i,j):
    Aux = np.array(PL.A[i])
    PL.A[i] = PL.A[j]
    PL.A[j] = Aux    
