class Symbol(object):
    Value = None
    Type = None
    Iden = None
    Locate = None

class LifeTime():
    Vars = {}

class SymbolTable(object):
    def __init__(self):
        self.tempBase = 't'
        self.tempNo = 0
        MainScope = LifeTime()
        self.scope = {'Main' : MainScope}
        self.CurrScope = 'Main'
    def create_temp(self):
        self.tempNo += 1
        return self.tempBase+str(self.tempNo-1)
    def isPresentIdent(self,key):
        return key in self.scope[self.CurrScope].Vars.keys()
    def addVar(self,var):
        self.scope[self.CurrScope].Vars[var.Iden]=var
    def getIdent(self,var):
        return self.scope[self.CurrScope].Vars[var]
