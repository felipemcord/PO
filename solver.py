import numpy as np
import sys

class LP:

    VariableNumber = 0
    RestrictionNumber = 0
    FPIVariables = 0
    E = []
    pivotLines = []
    Objective = []
    Restrictions = []
    FreeVariables = []
    A = []
    B = []

class LPNP:
    def __init__(self,PL):
        self.VariableNumber = PL.VariableNumber
        self.RestrictionNumber = PL.RestrictionNumber
        self.FPIVariables = PL.FPIVariables
        self.A = np.array(PL.A)
        self.E = np.identity(self.A.shape[0])
        self.Objective = np.array(PL.Objective)
        self.Restrictions = np.array(PL.Restrictions)
        self.B = np.array(PL.B)
        self.pivotLines = []
        self.pivotColumns = [0] * (self.RestrictionNumber + 1)

    VariableNumber = 0
    RestrictionNumber = 0
    FPIVariables = 0
    E = []
    pivotLines = []
    pivotColumns = []
    Objective = []
    Restrictions = []
    FreeVariables = []
    A = []
    B = []

def removeSmallNumbers(A):
    A[abs(A) < 10**(-10)] = 0
    return A

def Pivot(PL , i, j):
    E = np.identity(PL.A.shape[0])
    # print("pivot",i,j)

    if(PL.A[i,j] != 1):
        E[i,...] /= PL.A[i,j]
    
    for row in range(PL.A.shape[0]):
        if(PL.A[row,j] != 0 and row != i):
            E[row,i] = -(PL.A[row,j]/ PL.A[i,j] )
    PL.E = E.dot(PL.E)
    PL.A = removeSmallNumbers(E.dot(PL.A))
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

def CreateRestrictions(InputFile, PL):
    PL.Restrictions = []
    PL.B = []
    PL.FPIVariables = 0
    for i in range(PL.RestrictionNumber):
        Line = InputFile.readline().split()

        Restriction = [0]
        for Variable in range(PL.VariableNumber):
            if(Variable in PL.FreeVariables):
                Restriction.extend([float(Line[Variable] ),-float(Line[Variable])])
            else:
                Restriction.append(float(Line[Variable]))

        for Variable in range(PL.FPIVariables):
            Restriction.append(0)
        
        if(Line[PL.VariableNumber] == ">="):
            Restriction.append(-1)
            PL.Objective.append(0)
            PL.FPIVariables += 1
            for Array in PL.Restrictions:
                Array.append(0)
        elif(Line[PL.VariableNumber] == "<="):
            Restriction.append(1)
            PL.FPIVariables += 1
            PL.Objective.append(0)
            for Array in PL.Restrictions:
                Array.append(0)

        PL.Restrictions.append(Restriction)
        PL.B.append(float(Line[-1]))

    for Index,Restriction in enumerate(PL.Restrictions):
        Restriction.append(PL.B[Index])

    return PL.Restrictions
        

def CreateInputArray(file):
    PL = LP()
    InputFile = open(file,'r')
    PL.VariableNumber = int(InputFile.readline())
    PL.RestrictionNumber = int(InputFile.readline())
    
    PL.FreeVariables = []
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        if(int(Value) != 1):
            PL.FreeVariables.append(Variable)
    
    PL.Objective = [1]
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        if(Variable in PL.FreeVariables):
            PL.Objective.extend([float(Value),-float(Value)])
        else:
            PL.Objective.append(float(Value))
    # PL.Restrictions = CreateRestrictions(InputFile, VariableNumber, RestrictionNumber, FreeVariables, Objective)
    PL.Restrictions = CreateRestrictions(InputFile,PL)
    PL.Objective.append(0)
    PL.A = [PL.Objective]
    PL.A.extend(PL.Restrictions)
    return PL

def insertValueinMatrix(PL,value,pos):
    A = np.zeros((PL.A.shape[0],PL.A.shape[1] + 1))
    for i in range(PL.A.shape[0]):
        A[i] = np.insert(PL.A[i],pos,value)
    PL.A = A

def createAuxPL(PL):
    PLAux = LPNP(PL)
    PLAux.Objective = np.array([0] * PL.Objective.shape[0])
    PLAux.A[0] = PLAux.Objective
    for i in range(1,PL.A.shape[0]):
        if( PL.A[i,PL.pivotColumns[i]] * PL.A[i,-1] < 0):
            PLAux.A[i] *= PL.A[i,-1]/abs(PL.A[i,-1])
            insertValueinMatrix(PLAux,0,-1 )
            PLAux.A[i,-2] = 1
            PLAux.A[0,-2] = 1
    return PLAux



PL =  CreateInputArray(sys.argv[1])
PLNP = LPNP(PL)
np.set_printoptions(linewidth=200,precision=2,suppress=True)
Canon(PLNP)
PLAux = createAuxPL(PLNP)
# print("\n")
# print(PLNP.A)
# print("\n")
# print(PLAux.A)
# print("\n")
Canon(PLAux)
print(PLAux.A)  
# for Line,Column in enumerate(PLNP.pivotColumns ):
#     print(Line,Column)
