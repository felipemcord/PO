import LPs
import numpy as np
import sys
import Utility

def Pivot(PL , i, j):
    E = np.identity(PL.A.shape[0])
    # print("pivot",i,j)

    if(PL.A[i,j] != 1):
        E[i,...] /= PL.A[i,j]
    
    for row in range(PL.A.shape[0]):
        if(PL.A[row,j] != 0 and row != i):
            E[row,i] = -(PL.A[row,j]/ PL.A[i,j] )
    PL.E = E.dot(PL.E)
    PL.A = Utility.removeSmallNumbers(E.dot(PL.A))
    # print(PL.A,"\n")
    return PL

def Canon( PL ):
    firstLine = PL.A[0]
    PL.pivotLines = []
    for i in list(reversed(range(firstLine.shape[0] - 1))):
        column = PL.A[...,i]
        for j in range(1,column.shape[0]):
            if(column[j] != 0 and j not in PL.pivotLines):
                PL = Pivot(PL,j,i)
                PL.pivotLines.append(j)
                PL.pivotColumns[j] = i
                break
    return PL


def createAuxPL(PL):
    PLAux = LPs.LPNP(PL)
    PLAux.A[0] = np.zeros((PL.A.shape[1]))
    PLAux.A[0,0] = 1
    for i in range(1,PL.A.shape[0]):    
        Utility.insertValueinMatrix(PLAux,0,-1 )
        PLAux.A[i,-2] = 1
        PLAux.A[0,-2] = 1
    PLAux.Objective = PLAux.A[0]
    return PLAux

def Solve(PL):

    NotMaxColumns = np.where(PL.A[0,:-1] < 0 )[0]
    while(NotMaxColumns.shape[0] > 0 ):

        Column = NotMaxColumns[0]
        MinValue = sys.maxsize
        MinIndex = 0
        if(np.where(PL.A[1:,Column] > 0 )[0].shape[0] <= 0):
            return "Unbounded"

        for Index,(AJK,B) in enumerate(zip(PL.A[1:,Column],PL.A[1:,-1] )):
            if(AJK > 0 and B/AJK < MinValue):
                MinValue = B/AJK
                MinIndex = Index + 1
        Pivot(PL,MinIndex,Column)
        PL.pivotColumns[MinIndex] = Column
        NotMaxColumns = np.where(PL.A[0,:-1] < 0 )[0]
    return PL.A[0,-1]

def GetCanonWithAux(PL,PLAux):
    Utility.MakeIdentity(PLAux)
    for Line in range(1,PL.A.shape[0]):
        PL.A[Line] = np.append(PLAux.A[Line,:PL.A.shape[1] - 1],PLAux.A[Line,-1])
    for Line,Column in enumerate(PLAux.pivotColumns):
        Pivot(PL,Line,Column)
        # print(PL.A)

def getSolution(PL):
    GetCanonWithAux(PL,PL)
    Solution = np.array([0] * PL.A.shape[1])
    for Line,Column in enumerate(PL.pivotColumns ):
        Solution[Column] = PL.A[Line,-1]
    # print(Solution.T.dot(PL.Objective))