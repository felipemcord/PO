import numpy as np
import LPs

def CreateRestrictions(InputFile, PL):
    PL.Restrictions = []
    PL.B = []
    PL.FPIVariables = 0
    for i in range(PL.RestrictionNumber):
        Line = InputFile.readline().split()

        Restriction = []
        for Variable in range(PL.VariableNumber):
            Restriction.append(float(Line[Variable]))
        PL.RestrictionType.append(Line[PL.VariableNumber])
        PL.Restrictions.append(Restriction)
        PL.B.append(float(Line[-1]))

    return PL.Restrictions


def CreateInputArray(file):
    PL = LPs.LP()
    InputFile = open(file,'r')
    PL.VariableNumber = int(InputFile.readline())
    PL.RestrictionNumber = int(InputFile.readline())
    PL.FreeVariables = []
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        if(int(Value) != 1):
            PL.FreeVariables.append(Variable)
    
    PL.Objective = []
    Line = InputFile.readline().split()
    for Variable,Value in enumerate(Line):
        PL.Objective.append(-float(Value))
        
    PL.Restrictions = CreateRestrictions(InputFile,PL)
    return PL