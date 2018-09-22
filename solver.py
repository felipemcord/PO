import LPs
import CreateInput
import Solve
import numpy as np
import sys


PL =  CreateInput.CreateInputArray(sys.argv[1])
PLNP = LPs.LPNP(PL)
np.set_printoptions(linewidth=200,precision=2,suppress=True)
print(PLNP.A)
Solve.Canon(PLNP)
Solve.Solve(PLNP)
# PLAux = createAuxPL(PLNP)
# print("\n")
# print(PLNP.A)
# print("\n")
# print(PLAux.A)
# print(PLAux.Objective)
# print("\n")
# Canon(PLAux)
# print(PLAux.A)  
# print("\n")
# print(PLAux.A)
# print("\n")
for Line,Column in enumerate(PLNP.pivotColumns ):
    print(Line,Column,PLNP.A[Line,-1])
# getSolution(PLNP)




