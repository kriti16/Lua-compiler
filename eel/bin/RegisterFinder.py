class RegisterFinder(object):
    def __init__(self,DeadAlive,Nextuse):
        self.DeadAlive = DeadAlive
        self.NextUse = Nextuse
    def getRegE(self,Perm,RegDesc,AddrDesc,i):
        if len(RegDesc.EAX)==0:
            return 'EAX',RegDesc,AddrDesc
        elif len(RegDesc.EBX)==0:
            return 'EBX',RegDesc,AddrDesc
        elif len(RegDesc.ECX)==0:
            return 'ECX',RegDesc,AddrDesc
        elif len(RegDesc.EDX)==0:
            return 'EDX',RegDesc,AddrDesc
        elif len(RegDesc.ESI)==0:
            return 'ESI',RegDesc,AddrDesc
        elif len(RegDesc.EDI)==0:
            return 'EDI',RegDesc,AddrDesc
        else:
            regToSpl = self.findSpill(RegDesc,Perm,i)
            RegDesc,AddrDesc = self.storeMem(regToSpl,RegDesc,AddrDesc)
            return regToSpl,RegDesc,AddrDesc
    def getReg(self,Entry2,RegDesc,AddrDesc,i):
        reg_Y = -1
        try:
            reg_Y = AddrDesc[Entry2]
        except:
            pass
        try:
            if len(getattr(RegDesc,reg_Y)) == 1 and self.NextUse[i][Entry2] == -1:
                #print "FIST Part2",reg_Y,Entry2
                return reg_Y,RegDesc,AddrDesc
        except:
            pass
        if len(RegDesc.EAX)==0:
            return 'EAX',RegDesc,AddrDesc
        elif len(RegDesc.EBX)==0:
            return 'EBX',RegDesc,AddrDesc
        elif len(RegDesc.ECX)==0:
            return 'ECX',RegDesc,AddrDesc
        elif len(RegDesc.EDI)==0:
            return 'EDI',RegDesc,AddrDesc
        elif len(RegDesc.EDX)==0:
            return 'EDX',RegDesc,AddrDesc
        elif len(RegDesc.ESI)==0:
            return 'ESI',RegDesc,AddrDesc
        else:
            #print "B",len(RegDesc.EDX)
            regToSpl = self.findSpill(RegDesc,Entry2,i)
            #print regToSpl
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
                tempVar=getattr(RegDesc,reg_Z)
                tempVar.remove(Entry2)
                if tempVar==None:
                    setattr(RegDesc,reg_Z,[])
                else:
                    setattr(RegDesc,reg_Z,tempVar)
                print "\tMOVL %"+reg_Z+",%ECX"
            else:
                print "\tMOVL "+Entry2+",%ECX"
            setattr(RegDesc,'ECX',[Entry2])
            AddrDesc[Entry2]='ECX'
        return regToSpl,RegDesc,AddrDesc
    
    def findAltSpill(self,RegDesc,y,i):
        #for t in vars(RegDesc):
            #print "See downa"
            #print t,getattr(RegDesc,t)
        if y not in RegDesc.EAX:
            return 'EAX'
        else:
            return 'EBX'
    def findSpill(self,RegDesc,y,i):
        furthest_line = []
        #print vars(RegDesc)
        for t in vars(RegDesc):
            #print getattr(RegDesc,t)
            if getattr(RegDesc,t) != []:
                #print "***************************************"
                dct = {'reg':t,'use':self.getNextUse(getattr(RegDesc,t),i)}
                #print "#######################################################"
                #print dct
                #print "#########################################################"
                furthest_line.append(dct)
                #print furthest_line
        reg_Use = sorted(furthest_line, key=lambda k: k['use'],reverse=True)
        #print reg_Use,"furthest"
        return reg_Use[0]['reg']
    def storeMem(self,reg,regDesc,AddrDesc):
        #print regDesc,reg
        varReg = getattr(regDesc,reg)
        for var in varReg:
            #print var,varReg
            print "\tMOVL %"+reg+","+var
            AddrDesc[var] = None
        setattr(regDesc,reg,[])
        return regDesc,AddrDesc
    def getNextUse(self,var,start):
        try:
            us = self.NextUse[start][var[0]]
            #print self.NextUse[start]
            #print us
            if us == -1:
                us = float("inf")
            return us
        except Exception:
            pass
        for j in range(start,-1,-1):#len(self.DeadAlive)):
            #print self.NextUse
            #print j,var[0],var[0] in self.NextUse[j].keys(),self.NextUse[j].keys()
            try:
                us = self.NextUse[j][var[0]]
                if us == -1:
                    us = float("inf")
                #print self.DeadAlive[j][var[0]]
                #print us
                return us
            except Exception:
                pass
        return float("inf")
