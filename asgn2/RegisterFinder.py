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
        #if reg_Y != None:
        #    print "Reg Y is nnnnnnnn"+ str(getattr(RegDesc,reg_Y))
        try:
            if len(getattr(RegDesc,reg_Y)) == 1 and self.NextUse[i][Entry2] == -1:
                #print "FIST Part2"
                return reg_Y,RegDesc,AddrDesc
        except:
            pass
        if len(RegDesc.EAX)==0:
            return 'EAX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EBX',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'ECX',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'EDX',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'ESI',RegDesc,AddrDesc
        #if len(RegDesc.EBX)==0:
        #    return 'EDI',RegDesc,AddrDesc
        else:
            regToSpl = 'EAX'
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            return regToSpl,RegDesc,AddrDesc
            
    def storeMem(self,reg,regDesc,AddrDesc):
        print "I am in "
        varReg = getattr(regDesc,reg)
        for var in varReg:
            print "MOVL "+var+",%"+reg
            del AddrDesc[var]
        setattr(regDesc,reg,[])
        return regDesc,AddrDesc
