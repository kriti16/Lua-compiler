class RegisterFinder(object):
    def __init__(self,DeadAlive,Nextuse):
        self.DeadAlive = DeadAlive
        self.NextUse = Nextuse
    def getReg(self,ThreeOpCode,RegDesc,AddrDesc,i):
        Entry1 = ThreeOpCode.SymtabEntry1
        Entry2 = ThreeOpCode.SymtabEntry2
        Entry3 = ThreeOpCode.SymtabEntry3
        reg_Y = -1
        try:
            reg_Y = AddrDesc[Entry2]
             #print "Fist",reg_Y
        except:
            #print "No "+Entry2
            pass
        try:
            if len(getattr(RegDesc,reg_Y)) == 1 and self.NextUse[i][Entry2] == -1:
                #print "FIST Part2",reg_Y,Entry2
                return reg_Y,RegDesc,AddrDesc
        except:
            pass
        if len(RegDesc.EAX)==0:
            return 'EAX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EBX',RegDesc,AddrDesc
        #if len(RegDesc.ECX)==0:
        #    return 'ECX',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'EDX',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'ESI',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'EDI',RegDesc,AddrDesc
        else:
            regToSpl = self.findSpill(RegDesc,Entry2)
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            return regToSpl,RegDesc,AddrDesc
    
    def divModGetReg(self,ThreeOpCode,RegDesc,AddrDesc,i):
        Entry1 = ThreeOpCode.SymtabEntry1
        Entry2 = ThreeOpCode.SymtabEntry2
        Entry3 = ThreeOpCode.SymtabEntry3
        reg_Y = -1
        try:
            reg_Y = AddrDesc[Entry2]
        except:
            pass
        try:
            if len(getattr(RegDesc,reg_Y)) == 1 and self.NextUse[i][Entry2] == -1 and reg_Y=='EAX':
                #print "FIST Part2",reg_Y,Entry2
                return reg_Y,RegDesc,AddrDesc
        except:
            pass
        regToSpl = 'EAX'
        RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
        return regToSpl,RegDesc,AddrDesc
    def findSpill(self,RegDesc,y):
        if y not in RegDesc.EAX:
            return 'EAX'
        else:
            return 'EBX'
    def storeMem(self,reg,regDesc,AddrDesc):
        varReg = getattr(regDesc,reg)
        for var in varReg:
            print "MOVL %"+reg+","+var
            AddrDesc[var] = None
        setattr(regDesc,reg,[])
        return regDesc,AddrDesc
