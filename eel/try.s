.section .data
t6:
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

.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n" 
strfmt:  .asciz "%s\n"

 .globl main

main:

LEE1:
	MOVL $0,%EAX
	MOVL %EAX,t0
	CALL CreateDict
	MOVL %EAX,t1
	MOVL t1,%EAX
	MOVL %EAX,t1
	MOVL %EAX,t2
LEE5:
	MOVL t0,%EAX
	MOVL $20,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t0
	JL LEE3
LEE2:
	JMP LEE4
LEE3:
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL t0,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t3
	MOVL %EAX,t0
	JMP LEE5
LEE4:
	MOVL $1,%EAX
	MOVL t0,%EBX
	MOVL $0,%ECX
	CMP %ECX,%EBX
	MOVL %EAX,t4
	MOVL %EBX,t0
	JG LEE7
LEE6:
	JMP LEE8
LEE7:
	MOVL t0,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t5
	PUSHL t5
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	JMP LEE9
LEE8:
	MOVL t0,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t6
	PUSHL t6
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
LEE9:
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL $0,%EAX

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

