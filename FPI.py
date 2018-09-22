import numpy as np
import LPs

def RemoveFreeVariables(PL):
    NewObjective = np.array(PL.Objective)
    NewRestrictions = np.array(PL.Restrictions)
    for Variable,Value in enumerate(PL.Objective):
        if Variable in PL.FreeVariables:

            FPIPos = Variable + PL.FPIVariables + 1
            NewObjective = np.insert(NewObjective,FPIPos,-Value)

            Aux = np.zeros((PL.RestrictionNumber,NewRestrictions.shape[1] + 1))
            for i in range(PL.RestrictionNumber):
                Value = PL.Restrictions[i,Variable]
                Aux[i] = np.insert(NewRestrictions[i],FPIPos,-Value )

            NewRestrictions = Aux
            PL.FPIVariables += 1
    PL.Objective = NewObjective
    PL.Restrictions = NewRestrictions

def RemoveInequalties(PL):
    NewVariableCount = np.count_nonzero( np.array(PL.RestrictionType)  != "==")
    PL.Objective = np.append(PL.Objective, [0] * NewVariableCount)
    Pos1 = PL.VariableNumber + PL.FPIVariables
    NewRestrictions = np.zeros((PL.RestrictionNumber,PL.Restrictions.shape[1] + NewVariableCount) )
    for Line in range(PL.RestrictionNumber):
        NewRestrictions[Line] = np.append(PL.Restrictions[Line], [0] * NewVariableCount)
        if(PL.RestrictionType[Line] == ">="):
            NewRestrictions[Line,Pos1] = -1
            Pos1 += 1
        elif PL.RestrictionType[Line] == "<=":
            NewRestrictions[Line,Pos1] = 1
            Pos1 += 1
    PL.Restrictions = NewRestrictions
        

def MakeBAbs(PL):
    for Line in range(PL.RestrictionNumber):
        if(PL.B[Line] < 0):
            PL.Restrictions[Line] *= -1
            if(PL.RestrictionType[Line] == ">="):
                PL.RestrictionType[Line] = "<="
            elif PL.RestrictionType[Line] == "<=":
                PL.RestrictionType[Line] = ">="


def CreateTableau(PL):
    A = np.zeros((PL.RestrictionNumber + 1,PL.Restrictions.shape[1] + 2))
    A[0] = np.append([1], np.append(PL.Objective,0) )
    for Restriction in range(PL.RestrictionNumber):
        A[Restriction + 1] = np.append([0],np.append(PL.Restrictions[Restriction], abs(PL.B[Restriction]) ) )
    PL.A = A

def MakeFPI(PL):
    PLNP = LPs.LPNP(PL)
    RemoveFreeVariables(PLNP)
    MakeBAbs(PLNP)
    RemoveInequalties(PLNP)
    CreateTableau(PLNP)
    return LPs.LPNP(PLNP)
