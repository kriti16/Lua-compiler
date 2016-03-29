class Symbol(object):
    Value = None
    Type = None
    Iden = None
    Locate = None
    PosList = []
    NegList = []
    NextList = []
    Quad = -1
    
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
        try:
            return key.Iden in self.scope[self.CurrScope].Vars.keys()
        except:
            return False
    def addVar(self,var):
        self.scope[self.CurrScope].Vars[var.Iden]=var
    def getIdent(self,var):
        try:
            return self.scope[self.CurrScope].Vars[var.Iden]
        except:
            return False
