.section .data
x:
  .long 0
y:
  .long 0
z:
  .long 0

.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n"

 .globl main

main:

LEE1:
	MOVL $1,%EAX
	MOVL $3,%EBX
	PUSHL %EAX
	PUSHL %EBX
	MOVL %EAX,x
	MOVL %EBX,y
	CALL sum
	MOVL %EDX,z

LEE2:
	PUSHL z
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

sum:
	PUSHL %EBP
	MOVL %ESP,%EBP
	MOVL 8(%EBP),%EAX
	MOVL 12(%EBP),%EBX
	ADDL %EBX,%EAX
	MOVL %EAX,%EDX
	MOVL %EBP,%ESP
	POPL %EBP
	RET $4