class RegisterFinder(object):
    def __init__(self,DeadAlive,Nextuse):
        self.DeadAlive = DeadAlive
        self.NextUse = Nextuse
    def getReg(self,ThreeOpCode,RegDesc,AddDesc):
        Entry1 = ThreeOpCode.SymtabEntry1
        Entry2 = ThreeOpCode.SymtabEntry2
        Entry3 = ThreeOpCode.SymtabEntry3
        
        return 1
