import numpy as np
import LPs

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
    PL = LPs.LP()
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