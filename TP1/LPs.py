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
    RestrictionType = []

class LPNP:
    
    def __init__(self,PL):
        self.VariableNumber = PL.VariableNumber
        self.RestrictionNumber = PL.RestrictionNumber
        self.FPIVariables = PL.FPIVariables
        self.A = np.array(PL.A)
        self.E = np.identity(self.RestrictionNumber + 1)
        self.Objective = np.array(PL.Objective)
        self.Restrictions = np.array(PL.Restrictions)
        self.B = np.array(PL.B)
        self.pivotLines = []
        self.FreeVariables = PL.FreeVariables
        self.pivotColumns = [0] * (self.RestrictionNumber + 1)
        self.RestrictionType = np.array(PL.RestrictionType)

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
    Solution = []
    RestrictionType = []
