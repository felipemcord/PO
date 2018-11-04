import numpy as np
import cplex
import sys
from cplex.callbacks import MIPInfoCallback

class TimeLimitCallback(MIPInfoCallback):

    def __call__(self):
        if not self.aborted and self.has_incumbent():
            gap = 100.0 * self.get_MIP_relative_gap()
            timeused = self.get_time() - self.starttime
            if timeused > self.timelimit:
                print("Good enough solution at", timeused, "sec., gap =",
                      gap, "%, quitting.")
                self.aborted = True
                self.abort()

class CILP:

    def __init__(self,columns,rows):
        self.rows = rows
        self.columns = columns
        self.ub = np.ones(columns).tolist()
        self.lb = np.zeros(columns).tolist()
        self.rhs = np.ones(rows)
        self.ctype = "I" * columns
        self.sense = "E" * rows
        self.colnames = ["x" + str(i) for i in range(1,columns + 1)]
        self.rownames = ["r" + str(i) for i in range(1,rows + 1)]
        self.prob = cplex.Cplex()
        self.prob.objective.set_sense(self.prob.objective.sense.maximize)

        self.prob.linear_constraints.add(rhs=self.rhs, senses=self.sense,
                                names=self.rownames)
    
    def readColumn(self,ILP_FILE):
        line =  ILP_FILE.readline().split()
        # print(line)
        self.obj.append(int(line[0]))
        aux = int(line[1])
        cname = []
        cval = []
        for i in range(2,aux + 2):
            cname.append("r" + line[i])
            cval.append(1)
        self.c.append([cname,cval])

    def readColumns(self,ILP_FILE):
        for i in range(self.columns):
            self.readColumn(ILP_FILE)
    
    def setConst(self):
        print(len(self.obj), len(self.lb)  )
        self.prob.variables.add(obj=self.obj, lb=self.lb, ub=self.ub,
                       names=self.colnames, types=self.ctype, columns=self.c)
    
    def Solve(self):
        self.starttime = self.prob.get_time()
        self.prob.solve()
    
    def PrintSol(self):
        print()
        # solution.get_status() returns an integer code
        print("Solution status = ", self.prob.solution.get_status(), ":", end=' ')
        # the following line prints the corresponding string
        print(self.prob.solution.status[self.prob.solution.get_status()])
        print("Solution value  = ", self.prob.solution.get_objective_value())
        
    def WriteCplex(self):
        self.prob.write("sppcplex.lp")

    def setTimeLimit(self,limit):
        timelim_cb = self.prob.register_callback(TimeLimitCallback)
        timelim_cb.starttime = self.prob.get_time()
        timelim_cb.timelimit = limit
        timelim_cb.aborted = False
        self.timeLimit = timelim_cb
    
    def GetInfo(self):
        gap = 100 *self.prob.solution.MIP.get_mip_relative_gap()
        bestObj = self.prob.solution.MIP.get_best_objective()
        Time = self.prob.get_time() - self.starttime
        print(gap,bestObj,Time)

    starttime = 0
    timeLimit = None
    obj = []
    ub = []
    lb = []
    ctype = ""
    colnames = []
    rhs = []
    rownames = []
    sense = ""
    rows = 0
    columns = 0
    c = []
    prob = None

name = "sppus01"
if(len(sys.argv) == 2):
    name = sys.argv[1]

ILP_FILE = open(name,"r")
aux = ILP_FILE.readline().split()
rows = int(aux[0])
columns = int(aux[1])
OILP = CILP(columns,rows)

OILP.readColumns(ILP_FILE)
OILP.setConst()
OILP.WriteCplex()
# OILP.setTimeLimit(20)

OILP.Solve()

OILP.PrintSol()

OILP.GetInfo()

# OILP.PrintSol()



