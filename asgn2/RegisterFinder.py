class RegisterFinder(object):
    def __init__(self,DeadAlive,Nextuse):
        self.DeadAlive = DeadAlive
        self.NextUse = Nextuse
    def getReg(self,ThreeOpCode,RegDesc,AddrDesc):
        Entry1 = ThreeOpCode.SymtabEntry1
        Entry2 = ThreeOpCode.SymtabEntry2
        Entry3 = ThreeOpCode.SymtabEntry3
        reg_Y = -1
        try:
             reg_Y = AddDesc[Entry2]
        except:
            pass
        try:
            if len(RegDesc.regY) == 1 and self.NextUse[Entry2] == -1:
                return regY,RegDesc,AddrDesc
        except:
            pass
        if len(RegDesc.EAX)==0:
            return 'EAX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EBX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'ECX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EDX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'ESI',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EDI',RegDesc,AddrDesc
        else:
            regToSpl = 'EAX'
            RegDesc,AddrDesc = storeMem(regToSpl)
            return regToSpl
            
    def storeMem(self,reg,regDesc,AddrDesc):
        varReg = getattr(regDesc,reg)
        for var in varReg:
            print "movl "+var+","+reg
            del AddrDesc[var]
        setAddr(regDesc,reg,[])
        return regDesc,AddrDesc
