.PHONY: all clean

all: clean1 copy

copy:./src/lexer.py
	@mkdir bin
	@cp ./src/lexer.py ./bin/lexer.py	
	@cp ./src/parser.py ./bin/parser	
	@cp -r ./src/ply ./bin/ply
	@chmod +x ./bin/parser
	@echo "Everything is cool. Just like the weather"

clean1:
	@rm -rf bin

clean:
	@rm -rf bin
	@echo "Ho gaya saaf"
