.section .data

.section .text

.globl _start

_start:
	movl $1, %eax
	imul $10, %eax,%ebx
	int $0x80
	