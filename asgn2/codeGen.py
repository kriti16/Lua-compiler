from bitstring import Bits
i=0
def getReg():
	global i
	i=i+1
	return "R"+str(i)

def bestLocation(variable):
	# if AddressDescriptor[y][Regs]!=NULL:
	# 	return ("reg",AddressDescriptor[y][0])
	# else:
	# 	return ("mem",AddressDescriptor[y][Memory])
	#return ("reg","R2")
	return ("mem","0xf")

def genCode(x,op,y,z):
	xloc=getReg()
	x86instr=""
	if op=='+':
		try:
			check=int(y)
		except ValueError:
			try:
				check=int(z)
			except ValueError:											##x=var+var
				loc,yloc=bestLocation(y)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+yloc+",%"+xloc+"\n"
				else:
					x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
				loc,zloc=bestLocation(z)
				if loc=="reg":
					zlocFinal=zloc
				else:
					zlocFinal=getReg()
					x86instr=x86instr+"mov $"+zloc+",%"+zlocFinal+"\n"
					x86instr=x86instr+"mov (%"+zlocFinal+"),%"+zlocFinal+"\n"
				x86instr=x86instr+"add %"+zlocFinal+",%"+xloc

			else:														##x=var+int
				loc,yloc=bestLocation(y)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"add $"+str(hex(z))+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
					x86instr=x86instr+"add $"+str(hex(z))+",%"+xloc
		else:	
			try:
				check=int(z)
			except ValueError:											##x=int+var
				loc,zloc=bestLocation(z)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+zloc+",%"+xloc+"\n"
					x86instr=x86instr+"add $"+str(hex(y))+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+zloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
					x86instr=x86instr+"add $"+str(hex(y))+",%"+xloc
			else:														##x=int+int
				ans=int(y)+int(z)
				x86instr=x86instr+"mov $"+str(hex(ans))+",%"+xloc

	if op=='-':
		try:
			check=int(y)
		except ValueError:
			try:
				check=int(z)
			except ValueError:											##x=var-var
				loc,yloc=bestLocation(y)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+yloc+",%"+xloc+"\n"
				else:
					x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
				loc,zloc=bestLocation(z)
				if loc=="reg":
					zlocFinal=zloc
				else:
					zlocFinal=getReg()
					x86instr=x86instr+"mov $"+zloc+",%"+zlocFinal+"\n"
					x86instr=x86instr+"mov (%"+zlocFinal+"),%"+zlocFinal+"\n"
				x86instr=x86instr+"sub %"+zlocFinal+",%"+xloc

			else:														##x=var-int
				loc,yloc=bestLocation(y)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"sub $"+str(hex(z))+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
					x86instr=x86instr+"sub $"+str(hex(z))+",%"+xloc
		else:	
			try:
				check=int(z)
			except ValueError:											##x=int-var
				loc,zloc=bestLocation(z)								
				if loc=="reg":
					x86instr=x86instr+"mov %"+zloc+",%"+xloc+"\n"
					x86instr=x86instr+"sub $"+str(hex(y))+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+zloc+",%"+xloc+"\n"
					x86instr=x86instr+"mov (%"+xloc+"),%"+xloc+"\n"
					x86instr=x86instr+"sub $"+str(hex(y))+",%"+xloc
			else:														##x=int-int
				ans=int(y)-int(z)
				if ans<0:
					ans=Bits(int=ans,length=32)
				else:
					ans=hex(ans)
				x86instr=x86instr+"mov $"+str(ans)+",%"+xloc

	if op=='*':
		try:
			check=int(y)
		except ValueError:
			try:
				check=int(z)
			except ValueError:											##x=var*var
				locy,yloc=bestLocation(y)	
				locz,zloc=bestLocation(z)							
				if locy=="reg":
					x86instr=x86instr+"mov %"+yloc+",%"+xloc+"\n"
					if locz=="reg":
						x86instr=x86instr+"imul %"+yloc+",%"+zloc+",%"+xloc
					else:
						x86instr=x86instr+"mov $"+zloc+",%"+xloc+"\n"
						x86instr=x86instr+"imul %"+yloc+",(%"+xloc+"),%"+xloc
				else:
					if locz=="reg":
						x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
						x86instr=x86instr+"imul %"+zloc+",(%"+xloc+"),%"+xloc
					else:
						newReg=getReg()
						x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
						x86instr=x86instr+"mov %("+xloc+"),%"+xloc+"\n"
						x86instr=x86instr+"mov $"+zloc+",%"+newReg+"\n"
						x86instr=x86instr+"imul %"+xloc+",(%"+newReg+"),%"+xloc

			else:														##x=var*int
				loc,yloc=bestLocation(y)
				if z<0:
					z=Bits(int=z,length=32)
				else:
					z=hex(z)								
				if loc=="reg":
					x86instr=x86instr+"imul $"+str(z)+",%"+yloc+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+yloc+",%"+xloc+"\n"
					x86instr=x86instr+"imul $"+str(z)+",(%"+xloc+"),%"+xloc
		else:	
			try:
				check=int(z)
			except ValueError:											##x=int*var
				loc,zloc=bestLocation(z)
				if y<0:
					y=Bits(int=y,length=32)
				else:
					y=hex(y)								
				if loc=="reg":
					x86instr=x86instr+"imul $"+str(y)+",%"+zloc+",%"+xloc
				else:
					x86instr=x86instr+"mov $"+zloc+",%"+xloc+"\n"
					x86instr=x86instr+"imul $"+str(y)+",(%"+xloc+"),%"+xloc
			else:														##x=int*int
				ans=int(y)*int(z)										
				if ans<0:
					ans=Bits(int=ans,length=32)
				else:
					ans=hex(ans)
				x86instr=x86instr+"mov $"+str(ans)+",%"+xloc

	return x86instr


print genCode('x','*','y','x')

		


