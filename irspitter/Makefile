.PHONY: all clean

all: clean1 copy out
	@./eel
	@rm -rf out out.o out.s

copy:./src/lexer.py
	@cp -r ./src/ ./bin/
	@chmod +x ./bin/irspit
	@echo "Everything is cool. Unlike the weather"
	@./bin/irspit ./test.lua > testF.ir

clean1:
	@rm -rf bin

clean:
	@rm -rf bin
	@echo "Ho gaya saaf"
