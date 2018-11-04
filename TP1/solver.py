import LPs
import CreateInput
import Solve
import FPI
import Utility
import numpy as np
import sys
import Output

fileIN = sys.argv[1]
PL =  CreateInput.CreateInputArray(fileIN)

PLNP = FPI.MakeFPI(PL)
PLAux = Solve.createAuxPL(PLNP)
Solve.Canon(PLAux)
Value = Solve.Solve(PLAux)
if(Value == 0):
    Solve.GetCanonWithAux(PLNP,PLAux)
    Solve.CanonStart(PLNP)
    if(Solve.Solve(PLNP) == "Unbounded"):
        Output.Status(sys.argv[2],"ilimitada")
        Output.Cert(PLNP)
    else:
        Output.Status(sys.argv[2],"otimo")
        Output.WriteObjective(PLNP)
        Output.Cert(PLNP)
else:
        Output.Status(sys.argv[2],"inviavel")
        Output.Cert(PLNP)
