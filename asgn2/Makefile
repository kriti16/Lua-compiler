.PHONY: all

all: out
	./out

out: out.s
	as --gstabs out.s -32 -o out.o
	ld out.o -m elf_i386 -o out

out.s:
	python FinalRun.py  >out.s

clean:
	rm -rf out out.o out.s
