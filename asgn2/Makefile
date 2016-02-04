.PHONY: all

all: out
	./out

out: out.s
	as --gstabs --32 out.s  -o out.o
	gcc -m32 out.o -o out
	

out.s:
	python FinalRun.py input4.ir >out.s

clean:
	rm -rf out out.o out.s
