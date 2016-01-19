.PHONY: all clean

all: clean1 copy

copy:./src/lexer.py
	@mkdir bin
	@cp ./src/lexer.py ./bin/lexer
	@cp -r ./src/ply ./bin/ply
	@chmod +x ./bin/lexer
	@echo "Everything is cool. Just like the weather"

clean1:
	@rm -rf bin

clean:
	@rm -rf bin
	@echo "Ho gaya saaf"
	
