.PHONY: all

all: out
	@./out
	@rm -rf out out.o out.s

out: out.s
	@as --gstabs --32 out.s  -o out.o
	@gcc -m32 out.o -o out
	
out.s:
	@python FinalRun.py testF.ir > out.s
	@rm *.pyc

clean:
	@rm -rf out out.o out.s
