class RegisterFinder(object):
    def __init__(self,DeadAlive,Nextuse):
        self.DeadAlive = DeadAlive
        self.NextUse = Nextuse
    def getRegE(self,Perm,RegDesc,AddrDesc,i):
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
            regToSpl = self.findSpill(RegDesc,Perm)
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            return regToSpl,RegDesc,AddrDesc
    def getReg(self,Entry2,RegDesc,AddrDesc,i):
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
        if len(RegDesc.ECX)==0:
            return 'ECX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EDX',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'ESI',RegDesc,AddrDesc
        if len(RegDesc.EBX)==0:
            return 'EDI',RegDesc,AddrDesc
        else:
            regToSpl = self.findSpill(RegDesc,Entry2)
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            return regToSpl,RegDesc,AddrDesc
    
    def divModGetReg(self,Entry2,RegDesc,AddrDesc,i):
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

    def shiftGetReg(self,Entry2,RegDesc,AddrDesc,i):
        reg_Z = -1
        try:
            reg_Z = AddrDesc[Entry2]
        except:
            pass
        #if reg
        if reg_Z =='ECX':
            return reg_Y,RegDesc,AddrDesc
        else:
            regToSpl = 'ECX'
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            if reg_Z!=None:
                tempVar=getattr(RegDesc,reg_Z).remove(Entry2)
                print "\tMOVL %"+reg_Z+",%ECX"
            else:
                print "\tMOVL "+Entry2+",%ECX"
            setattr(RegDesc,'ECX',[Entry2])
            AddrDesc[Entry2]='ECX'
        
        return regToSpl,RegDesc,AddrDesc
    
    def findSpill(self,RegDesc,y):
        if y not in RegDesc.EAX:
            return 'EAX'
        else:
            return 'EBX'
    def storeMem(self,reg,regDesc,AddrDesc):
        varReg = getattr(regDesc,reg)
        for var in varReg:
            print "\tMOVL %"+reg+","+var
            AddrDesc[var] = None
        setattr(regDesc,reg,[])
        return regDesc,AddrDesc
