.PHONY: all

all: out
	@./out
	@rm -rf out out.o out.s

out: out.s
	@gcc -m32 out.s -o out

out.s: copy
	@./bin/FinalRun.py testF.ir > out.s
	
copy:./src/lexer.py
	@cp -r ./src/* ./bin
	@chmod +x ./bin/irspit
	@chmod +x ./bin/FinalRun.py
	@echo "Everything is cool. Unlike the weather"
	@./bin/irspit ./test.lua > testF.ir
	
clean:
	@rm -rf ./bin/*
	@rm  out.*
