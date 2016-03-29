from copy import deepcopy
class Symbol(object):
    def __init__(self):
        self.Value = None
        self.Type = None
        self.Iden = None
        self.Locate = None
        self.PosList = []
        self.NegList = []
        self.NextList = []
        self.Quad = -1
        self.Scope = None

    
class LifeTime(object):
    def __init__(self):
        self.Vars = {}
        self.Type = None
        self.Parent = None
    
class SymbolTable(object):
    def __init__(self):
        self.tempBase = 't'
        self.tempNo = 0
        self.scopeNum = 0
        MainScope = LifeTime()
        MainScope.Type = 'Main'
        self.scope = {'L0' : MainScope}
        self.CurrScope = 'L0'

    def create_Scope(self):
        self.scopeNum += 1
        scope_name = self.CurrScope + "_"+str(self.scopeNum)
        return scope_name
        
    def create_temp(self):
        self.tempNo += 1
        return self.tempBase+str(self.tempNo-1)


    def add_scope(self,Type):
        getName = self.create_Scope()
        tempSc = LifeTime()
        tempSc.Parent = self.CurrScope
        tempSc.Type = Type
        self.scope[getName] = tempSc
        self.CurrScope = getName
        
    def leave_scope(self):
        self.CurrScope = self.scope[self.CurrScope].Parent
    
    def findParent(self,scope):
        return "_".join(scope.split('_')[0:-1])
        
    def isPresentIdent(self,key,scope=None,stubborn=False):
        #scope is None at start
        if scope == None:
            scope = self.CurrScope
        try:
            if key.Iden in self.scope[scope].Vars.keys():
                return True
            elif scope == 'L0' or stubborn:
                return False
            else:
                par_scope = self.findParent(scope)
                return self.isPresentIdent(key,scope=par_scope)
        except:
            return False
        
    def getIdentScope(self,key,scope=None):
        #scope is None at start
        if scope == None:
            scope = self.CurrScope
        try:
            if key.Iden in self.scope[scope].Vars.keys():
                return scope
            elif scope == 'L0':
                return -1
            else:
                par_scope = self.findParent(scope)
                return self.getIdentScope(key,scope=par_scope)
        except:
            return -1

    
    def addVar(self,var,sc = None):
        if sc == None:
            sc = 'L0'
        self.scope[sc].Vars[var.Iden]=deepcopy(var)

        
    def getIdent(self,var, sc = None):
        if sc == None:
            sc = 'L0'
        #try:
        if self.isPresentIdent(var):
            sc = self.getIdentScope(var)
            return self.scope[sc].Vars[var.Iden]
        #except:
        #    return False
