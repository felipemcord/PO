import LPs
import numpy as np

Output = None

def Status(fileOut,Status):
    global Output
    Output = open(fileOut,'w')
    Output.write("Status: " + Status  + "\n")
    np.set_printoptions(precision=4,suppress=True)

def getObjective(PL):
    Objective = []
    Column = 1
    for Variable in range(PL.VariableNumber):
        if Variable in PL.FreeVariables:
            NegativeColumn = Column + 1
            if Column in PL.pivotColumns:
                Line = PL.pivotColumns.index(Column)
                Objective.append( PL.A[Line,-1] )
            elif NegativeColumn in PL.pivotColumns:
                Line = PL.pivotColumns.index(NegativeColumn)
                Objective.append( PL.A[Line,-1] )
            else:
                Objective.append(0)
            Column = NegativeColumn + 1
        
        else:
            if Column in PL.pivotColumns:
                Line = PL.pivotColumns.index(Column)
                Objective.append( PL.A[Line,-1] )
            else:
                Objective.append(0)
            Column += 1
    return Objective  


def WriteObjective(PL):
    np.set_printoptions(precision=4,suppress=True)
    Output.write("Objetivo: " + np.array2string(PL.A[1,-1],precision=4) + "\n")
    Output.write("Solucao:\n")

    Sol = ['{:.2f}'.format(x) for x in getObjective(PL) ]
    Output.write(" ".join(Sol) + "\n"  )
def Cert(PL):
    np.set_printoptions(precision=4,suppress=True)
    Output.write("Certificado:\n" )
    Output.write( np.array2string(PL.E[1,:] )[1:-1]  + "\n" )