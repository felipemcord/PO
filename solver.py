import LPs
import CreateInput
import Solve
import FPI
import Utility
import numpy as np
import sys

np.set_printoptions(precision=2,linewidth=200)
PL =  CreateInput.CreateInputArray('exemplo1.txt')
PLNP = FPI.MakeFPI(PL)
PLAux = Solve.createAuxPL(PLNP)
Solve.Canon(PLAux)
# print(PLNP.A)
Solve.Solve(PLAux)
# Utility.MakeIdentity(PLAux)
Solve.Canon(PLNP)
# Solve.GetCanonWithAux(PLNP,PLAux)
print(PLNP.A)
print(Solve.Solve(PLNP))
# print(PLAux.A[1:,:PLNP.A.shape[1] - 1])

