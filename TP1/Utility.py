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
            Aux = PL.pivotColumns[pivotLine]
            PL.pivotColumns[pivotLine] =  PL.pivotColumns[Line]
            PL.pivotColumns[Line] = Aux
        Line += 1
        

def SwitchLines(PL,i,j):
    E = np.identity(PL.A.shape[0])
    Aux = np.array(E[i])
    E[i] = E[j]
    E[j] = Aux   
    PL.E = E.dot(PL.E)
    PL.A = E.dot(PL.A) 
