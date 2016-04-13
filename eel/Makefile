.PHONY: all

all: out
	@./out
	#@rm -rf out out.o out.s

out: out.s
	@g++ -m32 -g -std=c++11 -w out.s Dict.cpp String.cpp -o out

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
