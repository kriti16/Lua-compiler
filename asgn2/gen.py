from helperScripts import *
from DataStruct import *

math_symbol={"+":"ADDL","-":"SUBL","*":"IMULL","/":"IDIVL","%":"IDIVL"}
cmp_symbol={">":"JG","<":"JL",">=":"JGE","<=":"JLE","==":"JE","~=":"JNE"}
def gen(ops,zdash,L):
	if ops.InstrType=="Math":
		opr=math_symbol[ops.Operator]
		if opr!="IDIVL":
			if check_variable(zdash):
				print "\t"+opr+" $"+str(zdash)+",%"+L
			elif zdash==ops.SymtabEntry3:
				print "\t"+opr+" "+zdash+",%"+L
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
		print "\tMOVL $1,%"+L
		if check_variable(z):
			print "\t+CMPL $"+str(z)+",%"+L
		elif zdash==ops.SymtabEntry3:
			print "\tCMPL "+zdash+",%"+L
		else:
			print "\tCMPL %"+zdash+",%"+L
		print "\t"+opr+" SKIP"
		print "\tMOVL $0,%"+L
		print "\nSKIP:\n"
		

if __name__=='__main__':
    op=ThreeOp()
    op.SymtabEntry3='z'
    op.Operator='/'
    gen(op,'EBX','EAX')
