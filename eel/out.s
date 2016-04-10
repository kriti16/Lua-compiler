.section .data
t8:
  .long 0
t9:
  .long 0
t6:
  .long 0
t7:
  .long 0
t4:
  .long 0
t5:
  .long 0
t2:
  .long 0
t3:
  .long 0
t0:
  .long 0
t1:
  .long 0
2:
  .long 0
t10:
  .long 0
t11:
  .long 0
t12:
  .long 0
_empty_:
  .long 0

.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n"

 .globl main

main:

LEE1:
	MOVL $2,%EAX
	MOVL %EAX,t0
LEE16:
	MOVL t0,%EAX
	MOVL $100,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t0
	JL LEE3
LEE2:
	JMP LEE4
LEE3:
	MOVL t0,%EAX
	MOVL $3,%ESI
	CDQ
	XOR %EDX,%EDX
	IDIVL %ESI
	 MOVL %EDX,%EAX
	MOVL $0,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t1
	JE LEE9
LEE5:
	JMP LEE7
LEE7:
	MOVL t0,%EAX
	MOVL $7,%ESI
	CDQ
	XOR %EDX,%EDX
	IDIVL %ESI
	 MOVL %EDX,%EAX
	MOVL $0,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t2
	JE LEE9
LEE8:
	JMP LEE10
LEE9:
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL t0,%EAX
	MOVL $23,%ESI
	CDQ
	XOR %EDX,%EDX
	IDIVL %ESI
	 MOVL %EDX,%EAX
	MOVL $0,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t3
	JE LEE12
LEE11:
	JMP LEE13
LEE12:
	MOVL t0,%EAX
	ADDL $10,%EAX
	MOVL %EAX,t4
	MOVL %EAX,t0
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL t0,%EAX
	ADDL $2,%EAX
	PUSHL $2
	PUSHL t0
	PUSHL %EAX
	MOVL %EAX,t10
	CALL f
	MOVL %EDX,t11
LEE14:
	PUSHL t11
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	JMP LEE4
LEE15:
	JMP LEE10
LEE13:
	JMP LEE10
LEE10:
	MOVL t0,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t12
	MOVL %EAX,t0
	JMP LEE16
LEE4:
	MOVL $0,%EAX
	MOVL %EAX,_empty_

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

f:
