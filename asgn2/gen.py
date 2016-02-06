from helperScripts import *
from DataStruct import *

math_symbol={"+":"ADDL","-":"SUBL","*":"IMULL","/":"IDIVL","%":"IDIVL",">>":"SARL","<<":"SALL"}
cmp_symbol={">":"JG","<":"JL",">=":"JGE","<=":"JLE","==":"JE","~=":"JNE"}
def gen(ops,zdash,L,i):
	if ops.InstrType=="Math":
		opr=math_symbol[ops.Operator]
		if opr!="IDIVL":
			if check_variable(zdash):
				print "\t"+opr+" $"+str(zdash)+",%"+L
			elif zdash==ops.SymtabEntry3:
				if opr=="SARL" or opr=="SALL":
					print "\t"+opr+" %CL,%"+L
				else:
					print "\t"+opr+" "+zdash+",%"+L
			else:
				if opr=="SARL" or opr=="SALL":
					print "\t"+opr+" %CL,%"+L
				else:
					print "\t"+opr+" %"+zdash+",%"+L
		else:
			print "\tMOVL $0,%EDX"
			if check_variable(ops.SymtabEntry3):
				print "\t"+opr+" %ESI"
			elif ops.SymtabEntry3==zdash:
				print "\t"+opr+" "+zdash
			else:
				print "\t"+opr+" %"+zdash
			if ops.Operator=='%':
				print "\t MOVL %EDX,%"+L

	elif ops.InstrType=="Compare":
		opr=cmp_symbol[ops.Operator]
		z=ops.SymtabEntry3
		if check_variable(z):
			print "\tCMPL $"+str(z)+",%"+L
		elif zdash==ops.SymtabEntry3:
			print "\tCMPL "+zdash+",%"+L
		else:
			print "\tCMPL %"+zdash+",%"+L
		print "\t"+opr+" GREAT"+str(i)
		print "\tMOVL $0,%"+L
                print "\tJMP Norm"+str(i)
		print "\nGREAT"+str(i)+":\n\tMOVL $1,%"+L
                print "\nNorm"+str(i)+":"
		

if __name__=='__main__':
    op=ThreeOp()
    op.SymtabEntry3='z'
    op.Operator='/'
    gen(op,'EBX','EAX')
